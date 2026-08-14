$base = "C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\2\Raw + wires + junctions"
$raw = Join-Path $base "raw -- schematic_image_variant_b_100.png"
$overlay = Join-Path $base "wire_nodes_overlay.png"
$out = Join-Path $base "codes\crops"
New-Item -ItemType Directory -Force -Path $out | Out-Null

Add-Type -AssemblyName System.Drawing

$crops = @(
    @{Name="raw_top_train_a"; Source=$raw; X=900; Y=420; W=4100; H=1450},
    @{Name="raw_top_tie"; Source=$raw; X=4700; Y=1180; W=900; H=420},
    @{Name="raw_top_train_b"; Source=$raw; X=5600; Y=420; W=3500; H=1450},
    @{Name="raw_loads_train_a_left"; Source=$raw; X=780; Y=1550; W=2700; H=3800},
    @{Name="raw_loads_train_a_right"; Source=$raw; X=3150; Y=1550; W=2050; H=4300},
    @{Name="raw_loads_train_b_left"; Source=$raw; X=5150; Y=1550; W=2850; H=3800},
    @{Name="raw_loads_train_b_right"; Source=$raw; X=7700; Y=1550; W=1700; H=4300},
    @{Name="raw_lower_rps"; Source=$raw; X=3300; Y=5000; W=5300; H=1500},
    @{Name="raw_title_notes"; Source=$raw; X=9000; Y=850; W=1550; H=6100},
    @{Name="overlay_top_train_a"; Source=$overlay; X=900; Y=420; W=4100; H=1450},
    @{Name="overlay_top_tie"; Source=$overlay; X=4700; Y=1180; W=900; H=420},
    @{Name="overlay_top_train_b"; Source=$overlay; X=5600; Y=420; W=3500; H=1450},
    @{Name="overlay_loads_train_a_left"; Source=$overlay; X=780; Y=1550; W=2700; H=3800},
    @{Name="overlay_loads_train_a_right"; Source=$overlay; X=3150; Y=1550; W=2050; H=4300},
    @{Name="overlay_loads_train_b_left"; Source=$overlay; X=5150; Y=1550; W=2850; H=3800},
    @{Name="overlay_loads_train_b_right"; Source=$overlay; X=7700; Y=1550; W=1700; H=4300},
    @{Name="overlay_lower_rps"; Source=$overlay; X=3300; Y=5000; W=5300; H=1500}
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
