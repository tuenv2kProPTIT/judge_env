

try:
    from ..sandbox.sandbox import IsolateSandbox as Sandbox
except:
    from sandbox.sandbox import IsolateSandbox as Sandbox



sandbox = Sandbox()

sandbox.cleanup()