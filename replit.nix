{ pkgs }: {
	deps = [
   pkgs.python-launcher
    pkgs.SDL2
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.xorg.libXinerama
    pkgs.xorg.libXcursor
    pkgs.xorg.libXrandr
    pkgs.xorg.libXi
    pkgs.xorg.libXxf86vm
  ];
}