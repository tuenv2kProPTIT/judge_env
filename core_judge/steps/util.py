import logging
try:
    from ..sandbox.sandbox import IsolateSandbox as Sandbox
    
    from ..config import env
except:
    from sandbox.sandbox import IsolateSandbox as Sandbox
    from config import env

logging.basicConfig(level=env.level_logging)
logger = logging.getLogger(__name__)



# TODO: stats grew enough to justify having a proper object representing them.


def execution_stats(sandbox, collect_output=False):
    """Extract statistics from a sandbox about the last ran command.
    sandbox (Sandbox): the sandbox to inspect.
    collect_output (bool): whether to collect output from the sandbox
        stdout_file and stderr_file.
    return (dict): a dictionary with statistics.
    """
    stats = {
        "execution_time": sandbox.get_execution_time(),
        "execution_wall_clock_time": sandbox.get_execution_wall_clock_time(),
        "execution_memory": sandbox.get_memory_used(),
        "exit_status": sandbox.get_exit_status(),
    }
    if stats["exit_status"] == Sandbox.EXIT_SIGNAL:
        stats["signal"] = sandbox.get_killing_signal()

    if collect_output:
        stats["stdout"] = sandbox.get_file_to_string(sandbox.stdout_file)\
            .decode("utf-8", errors="replace").strip()
        stats["stderr"] = sandbox.get_file_to_string(sandbox.stderr_file)\
            .decode("utf-8", errors="replace").strip()
    # print(stats)
    return stats


def merge_execution_stats(first_stats, second_stats, concurrent=True):
    """Merge two execution statistics dictionary.
    The first input stats can be None, in which case the second stats is copied
    to the output (useful to treat the first merge of a sequence in the same
    way as the others).
    first_stats (dict|None): statistics about the first execution; contains
        execution_time, execution_wall_clock_time, execution_memory,
        exit_status, and possibly signal.
    second_stats (dict): same for the second execution.
    concurrent (bool): whether to merge using assuming the executions were
        concurrent or not (see return value).
    return (dict): the merged statistics, using the following algorithm:
        * execution times are added;
        * memory usages are added (if concurrent) or max'd (if not);
        * wall clock times are max'd (if concurrent) or added (if not);
        * exit_status and related values (signal) are from the first non-OK,
            if present, or OK;
        * stdout and stderr, if present, are joined with a separator line.
    raise (ValueError): if second_stats is None.
    """
    if second_stats is None:
        raise ValueError("The second input stats cannot be None.")
    if first_stats is None:
        return second_stats.copy()

    ret = first_stats.copy()
    ret["execution_time"] += second_stats["execution_time"]

    if concurrent:
        ret["execution_wall_clock_time"] = max(
            ret["execution_wall_clock_time"],
            second_stats["execution_wall_clock_time"])
        ret["execution_memory"] += second_stats["execution_memory"]
    else:
        ret["execution_wall_clock_time"] += \
            second_stats["execution_wall_clock_time"]
        ret["execution_memory"] = max(ret["execution_memory"],
                                      second_stats["execution_memory"])

    if first_stats["exit_status"] == Sandbox.EXIT_OK:
        ret["exit_status"] = second_stats["exit_status"]
        if second_stats["exit_status"] == Sandbox.EXIT_SIGNAL:
            ret["signal"] = second_stats["signal"]

    for f in ["stdout", "stderr"]:
        if f in ret or f in second_stats:
            ret[f] = "\n===\n".join(d[f]
                                    for d in [ret, second_stats]
                                    if f in d)

    return ret

def _generic_execution(sandbox, command, exec_num, step_name,
                       collect_output=False):
    """A single command execution of a multi-command step.
    sandbox (Sandbox): the sandbox to use, already created and configured.
    command ([str]): command to execute.
    exec_num (int): 0-based index of the execution, to be used not to
        overwrite the output files.
    step_name (str): name of the step, also used as a prefix for the stdout
        and stderr files.
    collect_output (bool): if True, stats will contain stdout and stderr of the
        command (regardless, they are redirected to file inside the sandbox).
    return (dict|None): execution statistics, including standard output and
        error, or None in case of an unexpected sandbox error.
    """
    sandbox.stdin_file = None
    sandbox.stdout_file = "%s_stdout_%d.txt" % (step_name, exec_num)
    sandbox.stderr_file = "%s_stderr_%d.txt" % (step_name, exec_num)
    
    # logging.debug(step_name + exec_num)
    box_success = sandbox.execute_without_std(command, wait=True)
    # print(box_success,exec_num)
    if not box_success:
        logger.debug("Step '%s' aborted because of sandbox error in '%s' on "
                     "the %d-th command ('%r').",
                     step_name, sandbox.get_root_path(), exec_num + 1, command)
        return None

    return execution_stats(sandbox, collect_output=collect_output)


def generic_step(sandbox, commands, step_name, collect_output=False):
    """Execute some commands in the sandbox.
    Execute the commands sequentially in the (already created and configured)
    sandbox.
    Terminate early after a command if the sandbox fails, or the command does
    not terminate normally and with exit code 0.
    sandbox (Sandbox): the sandbox we consider, already created.
    commands ([[str]]): compilation commands to execute.
    step_name (str): used for logging and as a prefix to the output files
    collect_output (bool): if True, stats will contain stdout and stderr of the
        commands (regardless, they are redirected to file inside the sandbox).
    return (dict|None): execution statistics, including standard output and
        error, or None in case of an unexpected sandbox error.
    """
    logger.debug("Starting step '%s' in sandbox '%s' (%d commands).",
                 step_name, sandbox.get_root_path(), len(commands))
    stats = None
    # print("ger",commands)
    for exec_num, command in enumerate(commands):
        logging.debug(commands)
        this_stats = _generic_execution(sandbox, command, exec_num, step_name,
                                        collect_output=collect_output)
        if this_stats is None:
            return None

        stats = merge_execution_stats(stats, this_stats, concurrent=False)
        # Command error, also return immediately, but returning the stats.
        if stats["exit_status"] != Sandbox.EXIT_OK:
            break

    return stats