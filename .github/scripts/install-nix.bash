  sh -c <(curl -L https://nixos.org/nix/install) --yes --daemon --nix-extra-conf-file /dev/stdin <<EXTRA_NIX_CONF
  extra-experimental-features = nix-command flakes
  extra-substituters = https://openlane.cachix.org
  extra-trusted-public-keys = openlane.cachix.org-1:qqdwh+QMNGmZAuyeQJTH9ErW57OWSvdtuwfBKdS254E=
  EXTRA_NIX_CONF
