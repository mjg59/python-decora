# Protocol for firmware 6.4

## Test environment:

- **Device**: Leviton Decora DDMX1
- **Version**: 6.4
- **Datetime**: Aug. 7, 2021

## Descriptions

The fireware version `6.4` seems to change the key changing process.

Currently, there is an mistery byte appending to the KEY sent from Decora BLE pairing mode.

The actually KEY is now -

Say we have `KEY_FROM_BLE`, which is (still) four byte long.
The actually `KEY` - which to be sent to BLE for authentication - is the `KEY_FROM_BLE` appended by
the `THE_MISTRIOUS_BYTE`, it's five bytes long. i.e.,

KEY = KEY_FROM_BLE + THE_MISTRIOUS_BYTE


The captured traffic on the ATT stack around the auth (Handle 0x37, or "event"):

>
> 1. ...Auth starts
> 
> 1. Localhost -> BLE
>    Request Write: `0x37`, Value: _22 53 00 00 00 00 00_
>    
> 1. Localhost -> BLE
>    Request Read: `0x37`
>    Response: _22 53 **81 46 5C 76** 00_
>    
> 1. Localhost -> BLE
>    Request Write: `0x37`, Value: _22 53 **81 46 5C 76** 67_    
> 
> 1. Auth completes...  
>

In the above traffic sample,
`KEY_FROM_BLE`=`81 46 5C 76` (or `81 46 5C 76 00`)
`THE_MISTRIOUS_BYTE`=`0x67`
`KEY`=`81 46 5C 76 67`

Noted that, on the current Decora mobile app UI (both iOS and Android), the user can reset the current authentication and
re-authenticate. This will change the `KEY_FROM_BLE` as well as the `THE_MISTRIOUS_BYTE`. This will de-auth all the paired
devices.

![Screenshot to de-auth device](./deauth.png)
