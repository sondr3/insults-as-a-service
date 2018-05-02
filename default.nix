with import <nixpkgs> {};

pkgs.python36.withPackages (ps: with ps; [ spacy virtualenv pip flask-restful flask])
