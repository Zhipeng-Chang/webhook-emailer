Param(
    [string]$configFile
)
#This PowerShell script runs on the Docker-Container-CI build agent, 
# built by Dockerfile.build-server

#this file was copied from https://github.com/coe-google-apps-support/oct-portal/blob/master/k8s/scripts/build-k8s-deployment-file.ps1

$BUILD_BUILDID = (Get-ChildItem Env:BUILD_BUILDID).Value
$BUILD_SOURCESDIRECTORY = (Get-ChildItem Env:BUILD_SOURCESDIRECTORY).Value
$BUILD_ARTIFACTSTAGINGDIRECTORY = (Get-ChildItem Env:BUILD_ARTIFACTSTAGINGDIRECTORY).Value
Write-Host "BuildId is $BUILD_BUILDID"


$configFileFullName = [System.IO.Path]::Combine([System.IO.Path]::Combine($BUILD_SOURCESDIRECTORY, "k8s"), $configFile)

if (![System.IO.File]::Exists($configFileFullName)) {
    throw "Unable to find file at $configFileFullName";
}

#Output of ConvertFrom-Yaml is an OrderedDictionary
$od = Get-Content $configFileFullName | Out-String | ConvertFrom-Yaml

#Set the proper tag on the image
$imageName = $od.spec.template.spec.containers[0].image.ToString()
$tagIndex = $imageName.indexOf(":")
if ($tagIndex -gt 0) {
    $imageName = $imageName.SubString(0, $tagIndex) + ":v1.0." + $BUILD_BUILDID
} else {
    $imageName = $imageName + ":v1.0." + $BUILD_BUILDID
}

$od.spec.template.spec.containers[0]["image"] = $imageName

Write-Host ("$configFile" + ":")
$od.ToString()

Write-Host "Saving $configFile to $BUILD_ARTIFACTSTAGINGDIRECTORY"

($od | ConvertTo-Yaml)[1] > $BUILD_ARTIFACTSTAGINGDIRECTORY/$configFile