$base = "C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\1\Raw + wires + junctions"
$raw = Join-Path $base "raw -- schematic_image_clean_100_connected.png"
$overlay = Join-Path $base "wire_nodes_overlay.png"
$out = Join-Path $base "codes\crops"
New-Item -ItemType Directory -Force -Path $out | Out-Null

Add-Type -AssemblyName System.Drawing

$crops = @(
    @{Name="raw_top_A"; Source=$raw; X=430; Y=190; W=1230; H=560},
    @{Name="raw_top_B"; Source=$raw; X=1660; Y=190; W=1240; H=560},
    @{Name="raw_top_C"; Source=$raw; X=2900; Y=190; W=900; H=560},
    @{Name="raw_loads_A"; Source=$raw; X=500; Y=1030; W=1130; H=980},
    @{Name="raw_loads_B"; Source=$raw; X=1680; Y=1030; W=1120; H=980},
    @{Name="raw_loads_C"; Source=$raw; X=2900; Y=1030; W=900; H=980},
    @{Name="raw_dc_ups"; Source=$raw; X=500; Y=1900; W=2400; H=1000},
    @{Name="raw_xfmr_A"; Source=$raw; X=880; Y=600; W=360; H=540},
    @{Name="raw_xfmr_B"; Source=$raw; X=2080; Y=600; W=360; H=540},
    @{Name="raw_xfmr_C"; Source=$raw; X=3080; Y=600; W=360; H=540},
    @{Name="raw_tie_AB"; Source=$raw; X=1530; Y=390; W=380; H=190},
    @{Name="raw_tie_BC"; Source=$raw; X=2730; Y=390; W=420; H=190},
    @{Name="overlay_top_A"; Source=$overlay; X=430; Y=190; W=1230; H=560},
    @{Name="overlay_top_B"; Source=$overlay; X=1660; Y=190; W=1240; H=560},
    @{Name="overlay_top_C"; Source=$overlay; X=2900; Y=190; W=900; H=560},
    @{Name="overlay_loads_A"; Source=$overlay; X=500; Y=1030; W=1130; H=980},
    @{Name="overlay_loads_B"; Source=$overlay; X=1680; Y=1030; W=1120; H=980},
    @{Name="overlay_loads_C"; Source=$overlay; X=2900; Y=1030; W=900; H=980},
    @{Name="overlay_dc_ups"; Source=$overlay; X=500; Y=1900; W=2400; H=1000}
    ,@{Name="overlay_xfmr_A"; Source=$overlay; X=880; Y=600; W=360; H=540}
    ,@{Name="overlay_xfmr_B"; Source=$overlay; X=2080; Y=600; W=360; H=540}
    ,@{Name="overlay_xfmr_C"; Source=$overlay; X=3080; Y=600; W=360; H=540}
    ,@{Name="overlay_tie_AB"; Source=$overlay; X=1530; Y=390; W=380; H=190}
    ,@{Name="overlay_tie_BC"; Source=$overlay; X=2730; Y=390; W=420; H=190}
)

foreach ($crop in $crops) {
    $img = [System.Drawing.Image]::FromFile($crop.Source)
    try {
        $rect = New-Object System.Drawing.Rectangle($crop.X, $crop.Y, $crop.W, $crop.H)
        $bmp = New-Object System.Drawing.Bitmap($crop.W, $crop.H)
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        try {
            $g.DrawImage($img, 0, 0, $rect, [System.Drawing.GraphicsUnit]::Pixel)
            $path = Join-Path $out ($crop.Name + ".png")
            $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
            Write-Output $path
        } finally {
            $g.Dispose()
            $bmp.Dispose()
        }
    } finally {
        $img.Dispose()
    }
}
