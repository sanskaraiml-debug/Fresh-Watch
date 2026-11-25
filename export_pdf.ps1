$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoFalse
$pptxPath = "C:\Users\LENOVO\Desktop\expiry_project\FreshWatch_Presentation.pptx"
$pdfPath = "C:\Users\LENOVO\Desktop\expiry_project\FreshWatch_Presentation.pdf"

Write-Host "Opening presentation..."
$pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)

Write-Host "Saving as PDF..."
# 32 is the constant for ppSaveAsPDF
$pres.SaveAs($pdfPath, 32)
$pres.Close()
$ppt.Quit()

Write-Host "PDF Exported Successfully to $pdfPath"
