"""Secure Engine commands: attestation, closeregion, lock/unlock, gencert, provision, etc."""

from typing import Any

from pycommander_core.commands._base import BaseCommand


class SecurityCommand(BaseCommand):
  """Secure Engine commands."""

  def _get_general_args(self, **kwargs: Any) -> list[str]:
    args = []
    args += self._get_adapter_connection_args()
    args += self._get_debug_args()
    args += self._get_kwargs(**kwargs)
    return args

  def attestation(self, reset: bool = True, **kwargs: Any) -> dict:
    """Run Secure Engine attestation.

    Args:
      reset (bool): Reset device after operation.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    return self._run("security", "attestation", *args).output

  def closeregion(self,
                  index: int,
                  reset: bool = True,
                  codeversion: int | None = None,
                  **kwargs: Any) -> dict:
    """Close a Secure Engine region by index.

    Args:
      index (int): Region index to close.
      reset (bool): Reset device after operation.
      codeversion (int): Code version to set.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if codeversion is not None:
      args += ["--codeversion", str(codeversion)]
    return self._run("security", "closeregion", str(index), *args).output

  def disabledeviceerase(self, reset: bool = True, dryrun: bool = False, prompt: bool = True, **kwargs: Any) -> dict:
    """Disable device erase capability.

    Args:
      reset (bool): Reset device after operation.
      dryrun (bool): Show what would be done without doing it.
      prompt (bool): Show confirmation prompt.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if dryrun:
      args += ["--dryrun"]
    if not prompt:
      args += ["--noprompt"]
    return self._run("security", "disabledeviceerase", *args).output

  def disabletamper(self,
                    reset: bool = True,
                    store: bool = True,
                    cert: str | None = None,
                    cert_privkey: str | None = None,
                    command_key: str | None = None,
                    cert_signature: str | None = None,
                    command_signature: str | None = None,
                    authorization: str | None = None,
                    cert_pubkey: str | None = None,
                    disable_param: str | None = None,
                    **kwargs: Any) -> dict:
    """Disable tamper detection (cert/signature/authorization options).

    Args:
      reset (bool): Reset device after operation.
      store (bool): Store settings.
      cert (str): Certificate file.
      cert_privkey (str): Certificate private key.
      command_key (str): Command key file.
      cert_signature (str): Certificate signature file.
      command_signature (str): Command signature file.
      authorization (str): Authorization data.
      cert_pubkey (str): Certificate public key.
      disable_param (str): Disable parameter.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if not store:
      args += ["--nostore"]
    if cert is not None:
      args += ["--cert", cert]
    if cert_privkey is not None:
      args += ["--cert-privkey", cert_privkey]
    if command_key is not None:
      args += ["--command-key", command_key]
    if cert_signature is not None:
      args += ["--cert-signature", cert_signature]
    if command_signature is not None:
      args += ["--command-signature", command_signature]
    if authorization is not None:
      args += ["--authorization", authorization]
    if cert_pubkey is not None:
      args += ["--cert-pubkey", cert_pubkey]
    if disable_param is not None:
      args += ["--disable-param", disable_param]
    return self._run("security", "disabletamper", *args).output

  def erasedevice(self, reset: bool = True, dryrun: bool = False, **kwargs: Any) -> dict:
    """Erase device (Secure Engine).

    Args:
      reset (bool): Reset device after operation.
      dryrun (bool): Show what would be done without doing it.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if dryrun:
      args += ["--dryrun"]
    return self._run("security", "erasedevice", *args).output

  def fwupgrade(self,
                filename: str = "",
                reset: bool = True,
                address: int | None = None,
                prompt: bool = True,
                **kwargs: Any) -> dict:
    """Upgrade Secure Engine firmware.

    Args:
      filename (str): Firmware file path.
      reset (bool): Reset device after operation.
      address (int): Address for upgrade.
      prompt (bool): Show confirmation prompt.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if address is not None:
      args += ["--address", self._get_address_string(address)]
    if not prompt:
      args += ["--noprompt"]
    return self._run("security", "fwupgrade", filename, *args).output

  def fwupgradecheck(self, reset: bool = True, **kwargs: Any) -> dict:
    """Check if Secure Engine firmware upgrade is available.

    Args:
      reset (bool): Reset device after operation.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    return self._run("security", "fwupgradecheck", *args).output

  def genauth(self,
              outfile: str | None = None,
              store: bool = True,
              deviceserialno: str | None = None,
              reset: bool = True,
              **kwargs: Any) -> dict:
    """Generate authorization data.

    Args:
      outfile (str): Output file path.
      store (bool): Store on device.
      deviceserialno (str): Device serial number.
      reset (bool): Reset device after operation.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if outfile is not None:
      args += ["--outfile", outfile]
    if not store:
      args += ["--nostore"]
    if deviceserialno is not None:
      args += ["--deviceserialno", deviceserialno]
    if not reset:
      args += ["--noreset"]
    return self._run("security", "genauth", *args).output

  def gencert(self,
              outfile: str | None = None,
              store: bool = True,
              deviceserialno: str | None = None,
              reset: bool = True,
              cert_pubkey: str | None = None,
              authorization: str | None = None,
              command_key: str | None = None,
              extsign: bool = False,
              **kwargs: Any) -> dict:
    """Generate Secure Engine certificate.

    Args:
      outfile (str): Output file path.
      store (bool): Store on device.
      deviceserialno (str): Device serial number.
      reset (bool): Reset device after operation.
      cert_pubkey (str): Certificate public key file.
      authorization (str): Authorization data.
      command_key (str): Command key file.
      extsign (bool): Output for external signing.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if outfile is not None:
      args += ["--outfile", outfile]
    if not store:
      args += ["--nostore"]
    if deviceserialno is not None:
      args += ["--deviceserialno", deviceserialno]
    if not reset:
      args += ["--noreset"]
    if cert_pubkey is not None:
      args += ["--cert-pubkey", cert_pubkey]
    if authorization is not None:
      args += ["--authorization", authorization]
    if command_key is not None:
      args += ["--command-key", command_key]
    if extsign:
      args += ["--extsign"]
    return self._run("security", "gencert", *args).output

  def gencommand(self,
                 outfile: str | None = None,
                 store: bool = True,
                 reset: bool = True,
                 action: str | None = None,
                 disable_param: int | None = None,
                 unlock_param: str | None = None,
                 **kwargs: Any) -> dict:
    """Generate Secure Engine command (disable/unlock etc.).

    Args:
      outfile (str): Output file path.
      store (bool): Store on device.
      reset (bool): Reset device after operation.
      action (str): Command action.
      disable_param (int): Disable parameter.
      unlock_param (str): Unlock parameter.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if outfile is not None:
      args += ["--outfile", outfile]
    if not store:
      args += ["--nostore"]
    if not reset:
      args += ["--noreset"]
    if action is not None:
      args += ["--action", action]
    if disable_param is not None:
      args += ["--disable-param", str(disable_param)]
    if unlock_param is not None:
      args += ["--unlock-param", unlock_param]
    return self._run("security", "gencommand", *args).output

  def genconfig(self,
                outfile: str | None = None,
                store: bool = True,
              deviceserialno: str | None = None,
              reset: bool = True,
              **kwargs: Any) -> dict:
    """Generate Secure Engine config.

    Args:
      outfile (str): Output file path.
      store (bool): Store on device.
      deviceserialno (str): Device serial number.
      reset (bool): Reset device after operation.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if outfile is not None:
      args += ["--outfile", outfile]
    if not store:
      args += ["--nostore"]
    if deviceserialno is not None:
      args += ["--deviceserialno", deviceserialno]
    if not reset:
      args += ["--noreset"]
    return self._run("security", "genconfig", *args).output

  def genkey(self,
             type: str,
             outfile: str | None = None,
             privkey: str | None = None,
             pubkey: str | None = None,
             **kwargs: Any) -> dict:
    """Generate Secure Engine key.

    Args:
      type (str): Key type.
      outfile (str): Output file path.
      privkey (str): Private key file path.
      pubkey (str): Public key file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    args += ["--type", type]
    if outfile is not None:
      args += ["--outfile", outfile]
    if privkey is not None:
      args += ["--privkey", privkey]
    if pubkey is not None:
      args += ["--pubkey", pubkey]
    return self._run("security", "genkey", *args).output

  def getpath(self,
              reset: bool = True,
              deviceserialno: str | None = None,
              **kwargs: Any) -> dict:
    """Get Secure Engine path/certificate path.

    Args:
      reset (bool): Reset device after operation.
      deviceserialno (str): Device serial number.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if deviceserialno is not None:
      args += ["--deviceserialno", deviceserialno]
    return self._run("security", "getpath", *args).output

  def lock(self,
           reset: bool = True,
           dryrun: bool = False,
           trustzone: str | None = None,
           **kwargs: Any) -> dict:
    """Lock Secure Engine / device.

    Args:
      reset (bool): Reset device after operation.
      dryrun (bool): Show what would be done.
      trustzone (str): TrustZone config.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if dryrun:
      args += ["--dryrun"]
    if trustzone is not None:
      args += ["--trustzone", trustzone]
    return self._run("security", "lock", *args).output

  def lockconfig(self,
                 reset: bool = True,
                 secure_debug_unlock: str | None = None,
                 dryrun: bool = False,
                 prompt: bool = True,
                 **kwargs: Any) -> dict:
    """Lock Secure Engine config.

    Args:
      reset (bool): Reset device after operation.
      secure_debug_unlock (str): Secure debug unlock config.
      dryrun (bool): Show what would be done.
      prompt (bool): Show confirmation prompt.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if secure_debug_unlock is not None:
      args += ["--secure-debug-unlock", secure_debug_unlock]
    if dryrun:
      args += ["--dryrun"]
    if not prompt:
      args += ["--noprompt"]
    return self._run("security", "lockconfig", *args).output

  def otprollbackcount(self, reset: bool = True, **kwargs: Any) -> dict:
    """Read OTP rollback count.

    Args:
      reset (bool): Reset device after operation.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    return self._run("security", "otprollbackcount", *args).output

  def provision(self, reset: bool = True, sefw: str | None = None, **kwargs: Any) -> dict:
    """Provision Secure Engine.

    Args:
      reset (bool): Reset device after operation.
      sefw (str): Secure Engine firmware file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if sefw is not None:
      args += ["--sefw", sefw]
    return self._run("security", "provision", *args).output

  def readcert(self,
               cert_type: str,
               outfile: str | None = None,
               reset: bool = True,
               **kwargs: Any) -> dict:
    """Read Secure Engine certificate.

    Args:
      cert_type (str): Certificate type to read.
      outfile (str): Output file path.
      reset (bool): Reset device after operation.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if outfile is not None:
      args += ["--outfile", outfile]
    if not reset:
      args += ["--noreset"]
    return self._run("security", "readcert", cert_type, *args).output

  def readconfig(self, reset: bool = True, **kwargs: Any) -> dict:
    """Read Secure Engine config.

    Args:
      reset (bool): Reset device after operation.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    return self._run("security", "readconfig", *args).output

  def readkey(self,
              sign: bool = False,
              command: bool = False,
              outfile: str | None = None,
              reset: bool = True,
              store: bool = True,
              **kwargs: Any) -> dict:
    """Read Secure Engine key (sign/command key).

    Args:
      sign (bool): Read sign key.
      command (bool): Read command key.
      outfile (str): Output file path.
      reset (bool): Reset device after operation.
      store (bool): Store on device.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if sign:
      args += ["--sign"]
    if command:
      args += ["--command"]
    if outfile is not None:
      args += ["--outfile", outfile]
    if not reset:
      args += ["--noreset"]
    if not store:
      args += ["--nostore"]
    return self._run("security", "readkey", *args).output

  def readregionconfig(self,
                       outfile: str | None = None,
                       reset: bool = True,
                       **kwargs: Any) -> dict:
    """Read code region configuration from the device. Series 3 only.

    Args:
      outfile (str): Output file path.
      reset (bool): Reset device after operation.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if outfile is not None:
      args += ["--outfile", outfile]
    if not reset:
      args += ["--noreset"]
    return self._run("security", "readregionconfig", *args).output

  def rollchallenge(self, reset: bool = True, store: bool = True, **kwargs: Any) -> dict:
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if not store:
      args += ["--nostore"]
    return self._run("security", "rollchallenge", *args).output

  def status(self,
             reset: bool = True,
             trustzone: bool = False,
             verbose: bool = False,
             **kwargs: Any) -> dict:
    """Read Secure Engine status.

    Args:
      reset (bool): Reset device after operation.
      trustzone (bool): Include TrustZone info.
      verbose (bool): Verbose output.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if trustzone:
      args += ["--trustzone"]
    if verbose:
      args += ["--verbose"]
    return self._run("security", "status", *args).output

  def transitiontodevelopment(self,
                              reset: bool = True,
                              dryrun: bool = False,
                              prompt: bool = True,
                              **kwargs: Any) -> dict:
    """Transition device to development (unlock for debug).

    Args:
      reset (bool): Reset device after operation.
      dryrun (bool): Show what would be done.
      prompt (bool): Show confirmation prompt.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if dryrun:
      args += ["--dryrun"]
    if not prompt:
      args += ["--noprompt"]
    return self._run("security", "transitiontodevelopment", *args).output

  def unlock(self,
             reset: bool = True,
             store: bool = True,
             cert: str | None = None,
             cert_privkey: str | None = None,
             command_key: str | None = None,
             cert_signature: str | None = None,
             command_signature: str | None = None,
             authorization: str | None = None,
             cert_pubkey: str | None = None,
             unlock_param: str | None = None,
             **kwargs: Any) -> dict:
    """Unlock Secure Engine (cert/signature/authorization options).

    Args:
      reset (bool): Reset device after operation.
      store (bool): Store on device.
      cert (str): Certificate file.
      cert_privkey (str): Certificate private key.
      command_key (str): Command key file.
      cert_signature (str): Certificate signature file.
      command_signature (str): Command signature file.
      authorization (str): Authorization data.
      cert_pubkey (str): Certificate public key.
      unlock_param (str): Unlock parameter.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    if not store:
      args += ["--nostore"]
    if cert is not None:
      args += ["--cert", cert]
    if cert_privkey is not None:
      args += ["--cert-privkey", cert_privkey]
    if command_key is not None:
      args += ["--command-key", command_key]
    if cert_signature is not None:
      args += ["--cert-signature", cert_signature]
    if command_signature is not None:
      args += ["--command-signature", command_signature]
    if authorization is not None:
      args += ["--authorization", authorization]
    if cert_pubkey is not None:
      args += ["--cert-pubkey", cert_pubkey]
    if unlock_param is not None:
      args += ["--unlock-param", unlock_param]
    return self._run("security", "unlock", *args).output

  def writeconfig(self,
                  store: bool = True,
                  reset: bool = True,
                  dryrun: bool = False,
                  prompt: bool = True,
                  configfile: str | None = None,
                  **kwargs: Any) -> dict:
    """Write Secure Engine config to device.

    Args:
      store (bool): Store on device.
      reset (bool): Reset device after operation.
      dryrun (bool): Show what would be done.
      prompt (bool): Show confirmation prompt.
      configfile (str): Config file path.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not store:
      args += ["--nostore"]
    if not reset:
      args += ["--noreset"]
    if dryrun:
      args += ["--dryrun"]
    if not prompt:
      args += ["--noprompt"]
    if configfile is not None:
      args += ["--configfile", configfile]
    return self._run("security", "writeconfig", *args).output

  def writekey(self,
               sign_keyfile: str | None = None,
               command_keyfile: str | None = None,
               decrypt_keyfile: str | None = None,
               reset: bool = True,
               store: bool = True,
               prompt: bool = True,
               dryrun: bool = False,
               **kwargs: Any) -> dict:
    """Write Secure Engine key(s) to device.

    Args:
      sign_keyfile (str): Sign key file path.
      command_keyfile (str): Command key file path.
      decrypt_keyfile (str): Decrypt key file path.
      reset (bool): Reset device after operation.
      store (bool): Store on device.
      prompt (bool): Show confirmation prompt.
      dryrun (bool): Show what would be done.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if sign_keyfile is not None:
      args += ["--sign", sign_keyfile]
    if command_keyfile is not None:
      args += ["--command", command_keyfile]
    if decrypt_keyfile is not None:
      args += ["--decrypt", decrypt_keyfile]
    if not reset:
      args += ["--noreset"]
    if not store:
      args += ["--nostore"]
    if not prompt:
      args += ["--noprompt"]
    if dryrun:
      args += ["--dryrun"]
    return self._run("security", "writekey", *args).output

  def writeregionconfig(self, file: str, reset: bool = True, **kwargs: Any) -> dict:
    """Write code region configuration to the device. Series 3 only.

    Args:
      file (str): Region config file path.
      reset (bool): Reset device after operation.

    Returns:
      Command output as parsed JSON (dict).
    """
    args = self._get_general_args(**kwargs)
    if not reset:
      args += ["--noreset"]
    return self._run("security", "writeregionconfig", file, *args).output
