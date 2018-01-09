print( 'Detecting CUDA based GPUs' )
#import pycuda.driver as cuda
#import pycuda.autoinit
from py3nvml.py3nvml import *

nvmlInit()

nvmlDevices = nvmlDeviceGetCount()

print( 'Cuda Devices Detected: %d' % ( nvmlDevices ) )

for devicenum in range( nvmlDevices ):
    handle = nvmlDeviceGetHandleByIndex( devicenum )
    pciInfo = nvmlDeviceGetPciInfo( handle )
    print( '%d: %s' % ( devicenum, nvmlDeviceGetName( handle ) ) )
    print( '     Bus ID: %d ' % ( pciInfo.bus ) )
    print( '     Device ID: %d' % ( pciInfo.pciDeviceId ) )
    print( '     Sub Device ID: %d' % ( pciInfo.pciSubSystemId ) )
    print( '     UUID: %s' % ( nvmlDeviceGetUUID( handle )  ) )
    print( '     Temperature: %dc' % ( nvmlDeviceGetTemperature( handle, NVML_TEMPERATURE_GPU ) ) )
    print( '     Fan Speed: %d%%' % ( nvmlDeviceGetFanSpeed( handle ) ) )
    print( '     Power Usage: %d watts' % ( nvmlDeviceGetPowerUsage( handle ) / 1000 ) ) #power usage returned in milliwatts

nvmlShutdown()

'''
cudaDevices = cuda.Device.count()

print( 'Cuda Devices Detected: %d' % ( cudaDevices ) )

for devicenum in range( cudaDevices ):
    device = cuda.Device( devicenum )
    attrs = device.get_attributes()

    print( '%d: Bus ID: %d Name: %s' % ( devicenum, device.get_attribute( cuda.device_attribute.PCI_BUS_ID ), device.name() ) )
    for method in vars(device).items():
        print( method )
'''