"""Solplanet client for solplanet integration."""

from dataclasses import asdict, dataclass
from enum import Enum
from json import dumps
import logging

import aiohttp

__author__ = "Zbigniew Motyka"
__copyright__ = "Zbigniew Motyka"
__license__ = "MIT"

_LOGGER = logging.getLogger(__name__)


@dataclass
class GetMeterDataResponse:
    """Get meter data response model.

    Attributes
    ----------
    flg : int
        TBD ??
    tim : str
        Datetime in format YYYYMMDDHHMMSS
    pac : int
        AC real power [W]
    itd : int
        Input today
    otd : int
        Output today
    iet : int
        Input total
    oet : int
        Output total
    mod : int
        TBD ??
    enb : int
        TBD ??

    """

    flg: int
    tim: str
    pac: int
    itd: int
    otd: int
    iet: int
    oet: int
    mod: int
    enb: int


@dataclass
class GetInverterDataResponse:
    """Get inverter data response model.

    Attributes
    ----------
    flg : int
        TBD ??
    tim : str
        Datetime in format YYYYMMDDHHMMSS
    tmp : int
        Inverter temperature [C]
    fac : int
        AC frequency [Hz]
    pac : int
        AC real power [W]
    sac : int
        AC apparent power [VA]
    qac : int
        AC reactive / complex power [VAR]
    eto : int
        Energy produced total [kWh]
    etd : int
        Energy produced today [kWh]
    hto : int
        Total running time [h]
    pf : int
        Power factor
    wan : int
        TBD ??
    err : int
        Error
    vac : list[int]
        AC voltages [V]
    iac : list[int]
        AC current [A]
    vpv : list[int]
        DC voltages [V]
    ipv : list[int]
        DC current [A]
    str : list[int]
        TBD ??

    """

    flg: int
    tim: str
    tmp: int
    fac: int
    pac: int
    sac: int
    qac: int
    eto: int
    etd: int
    hto: int
    pf: int
    wan: int
    err: int
    vac: list[int]
    iac: list[int]
    vpv: list[int]
    ipv: list[int]
    str: list[int]


@dataclass
class GetBatteryDataResponse:
    """Get battery data response model.

    Attributes
    ----------
    flg : int
        TBD ??
    tim : str
        Datetime in format YYYYMMDDHHMMSS
    vb : int
        Battery voltage [cV]
    cb : int
        Battery current [dV]
    pb : int
        Power pattery [W]
    tb : int
        Temperature [dC]
    soc : int
        State of charge [%]
    soh : int
        State of health [%]

    """

    flg: int
    tim: str
    ppv: int
    etdpv: int
    etopv: int
    cst: int
    bst: int
    eb1: int
    wb1: int
    vb: int
    cb: int
    pb: int
    tb: int
    soc: int
    soh: int
    cli: int
    clo: int
    ebi: int
    ebo: int
    eaci: int
    eaco: int
    vesp: int
    cesp: int
    fesp: int
    pesp: int
    rpesp: int
    etdesp: int
    etoesp: int
    charge_ac_td: int
    charge_ac_to: int


@dataclass
class GetMonitorInfoResponse:
    """Get monitor info response."""

    psn: str
    key: str
    typ: int
    nam: str
    mod: str
    muf: str
    brd: str
    hw: str
    sw: str
    wsw: str
    protocol: str
    tim: str
    drm: int
    drm_q: int
    ali_ip: str
    ali_port: int
    pdk: str
    ser: str  # codespell:ignore ser
    status: int


@dataclass
class GetInverterInfoItemResponse:
    """Get inverter info item response."""

    isn: str
    add: int
    safety: int
    rate: int
    msw: str
    ssw: str
    tsw: str
    pac: int
    etd: int
    eto: int
    err: int
    cmv: str
    mty: int
    model: str


@dataclass
class GetInverterInfoResponse:
    """Get inverter info response."""

    inv: list[GetInverterInfoItemResponse]
    num: int


@dataclass
class GetRegulateInfoResponse:
    """Get regulate info response."""

    mod: int
    enb: int
    exp_m: int
    regulate: int
    enb_PF: int  # noqa: N815
    target_PF: int  # noqa: N815
    total_pac: int
    total_fac: int
    meter_pac: int


@dataclass
class GetBatteryInfoItemResponse:
    """Get battery info item response."""

    bid: int
    devtype: str
    manufactoty: str
    partno: str
    model1sn: str
    model2sn: str
    model3sn: str
    model4sn: str
    model5sn: str
    model6sn: str
    model7sn: str
    model8sn: str
    modeltotal: int
    monomertotoal: int
    monomerinmodel: int
    ratedvoltage: int
    capacity: int
    hardwarever: str
    softwarever: str


@dataclass
class GetBatteryInfoResponse:
    """Get battery data response model.

    Attributes
    ----------
    charge_max : int
        Max charge battery level [%]
    discharge_max : int
        Max discharge battery level [%]

    """

    isn: str
    stu_r: int
    type: int
    mod_r: int
    muf: int
    mod: int
    num: int
    fir_r: int
    charging: int
    charge_max: int
    discharge_max: int
    battery: GetBatteryInfoItemResponse


@dataclass
class GetWifiListItemResponse:
    """Get Wifi list item response."""

    sid: str
    srh: str
    channel: str


@dataclass
class GetWifiListResponse:
    """Get Wifi list response."""

    wif: list[GetWifiListItemResponse]
    num: str


@dataclass
class GetWlanStaInfoResponse:
    """Get wlan sta info response."""

    mode: str
    sid: str
    srh: int
    ip: str
    gtw: str
    msk: str


@dataclass
class GetWlanApInfoResponse:
    """Get wlan ap info response."""

    mode: str
    sid: str
    psw: str
    ip: str


class BatteryMode(Enum):
    """Battery mode."""

    OwnNeeds = 1
    Backup = 2
    Advanced = 3
    OffGrid = 4
    Charging = 5


@dataclass
class SetBatteryConfigValueRequest:
    """Set battery config value request."""

    type: int
    mod_r: int
    sn: str
    discharge_max: int
    charge_max: int
    muf: int
    mod: int
    num: int


@dataclass
class SetBatteryConfigRequest:
    """Set battery config request."""

    value: SetBatteryConfigValueRequest
    device: int = 4
    action: str = "setbattery"


@dataclass
class GetWlanInfoResponse:
    """Get wlan info response."""

    mode: str
    ip: str
    gtw: str
    msk: str


class SolplanetClient:
    """Solplanet http client."""

    def __init__(self, host: str) -> None:
        """Create instance of solplanet http client."""
        self.host = host
        self.port = 8484

    def get_url(self, endpoint: str) -> str:
        """Get URL for specified endpoint."""
        return "http://" + self.host + ":" + str(self.port) + "/" + endpoint

    async def get(self, endpoint: str):
        """Make get request to specified endpoint."""
        session = aiohttp.ClientSession()
        response = await session.get(self.get_url(endpoint))
        result = await response.json()
        await session.close()
        return result


class SolplanetApi:
    """Solplanet api v2 client."""

    def __init__(self, client: SolplanetClient) -> None:
        """Create instance of solplanet api."""
        _LOGGER.debug("Creating api instance")
        self.client = client

    async def get_meter_data(self) -> GetMeterDataResponse:
        """Get meter data."""
        _LOGGER.debug("Getting meter data")
        response = await self.client.get("getdevdata.cgi?device=3")
        return GetMeterDataResponse(**response)

    async def get_inverter_data(self, sn: str) -> GetInverterDataResponse:
        """Get inverter data."""
        _LOGGER.debug("Getting inverter (%s) data", sn)
        response = await self.client.get("getdevdata.cgi?device=2&sn=" + sn)
        return GetInverterDataResponse(**response)

    async def get_battery_data(self, sn: str) -> GetBatteryDataResponse:
        """Get battery data."""
        _LOGGER.debug("Getting battery (%s) data", sn)
        response = await self.client.get("getdevdata.cgi?device=4&sn=" + sn)
        return GetBatteryDataResponse(**response)

    async def get_monitor_info(self) -> GetMonitorInfoResponse:
        """Get monitor info."""
        _LOGGER.debug("Getting monitor info")
        response = await self.client.get("getdev.cgi")
        return GetMonitorInfoResponse(**response)

    async def get_inverter_info(self) -> GetInverterInfoResponse:
        """Get inverter info."""
        _LOGGER.debug("Getting inverter info")
        response = await self.client.get("getdev.cgi?device=2")
        response["inv"] = [
            GetInverterInfoItemResponse(**item) for item in response["inv"]
        ]
        return GetInverterInfoResponse(**response)

    async def get_regulate_info(self) -> GetRegulateInfoResponse:
        """Get regulate info."""
        _LOGGER.debug("Getting regulate info")
        response = await self.client.get("getdev.cgi?device=3")
        return GetRegulateInfoResponse(**response)

    async def get_battery_info(self) -> GetBatteryInfoResponse:
        """Get battery info."""
        _LOGGER.debug("Getting battery info")
        response = await self.client.get("getdev.cgi?device=4")
        response["battery"] = GetBatteryInfoItemResponse(**response["battery"])
        return GetBatteryInfoResponse(**response)

    async def get_wifi_list(self) -> GetWifiListResponse:
        """Get available wifi networks list."""
        _LOGGER.debug("Getting wifi list")
        response = await self.client.get("wlanget.cgi?info=4")
        response["wif"] = [GetWifiListItemResponse(**item) for item in response["wif"]]
        return GetWifiListResponse(**response)

    async def get_wlan_sta_info(self) -> GetWlanStaInfoResponse:
        """Get WLAN STA info."""
        _LOGGER.debug("Getting sta info")
        response = await self.client.get("wlanget.cgi?info=2")
        return GetWlanStaInfoResponse(**response)

    async def get_wlan_ap_info(self) -> GetWlanApInfoResponse:
        """Get WLAN AP info."""
        _LOGGER.debug("Getting ap info")
        response = await self.client.get("wlanget.cgi?info=1")
        return GetWlanApInfoResponse(**response)

    async def get_wlan_info(self) -> GetWlanInfoResponse:
        """Get wlan info."""
        _LOGGER.debug("Getting wlan info")
        response = await self.client.get("wlanget.cgi?info=3")
        return GetWlanInfoResponse(**response)

    async def set_battery_config(self, request: SetBatteryConfigRequest) -> None:
        """Set battery config."""
        _LOGGER.debug("Set battery config: %s", dumps(asdict(request)))

    async def change_battery_mode(self, mode: BatteryMode) -> None:
        """Change battery mode."""
        current = await self.get_battery_info()
        value = SetBatteryConfigValueRequest(
            type=current.type,
            mod_r=current.mod_r,
            muf=current.muf,
            mod=current.mod,
            num=current.num,
            sn=current.isn,
            charge_max=current.charge_max,
            discharge_max=current.discharge_max,
        )
        self._fill_set_battery_config_value_request(value, mode)
        request = SetBatteryConfigRequest(value=value)
        await self.set_battery_config(request)

    def _fill_set_battery_config_value_request(
        self, battery_value: SetBatteryConfigValueRequest, mode: BatteryMode
    ) -> SetBatteryConfigValueRequest:
        if mode == BatteryMode.OwnNeeds:
            battery_value.mod_r = 2
            battery_value.type = 1
        elif mode == BatteryMode.Backup:
            battery_value.mod_r = 3
            battery_value.type = 1
        elif mode == BatteryMode.Advanced:
            battery_value.mod_r = 4
            battery_value.type = 1
        elif mode == BatteryMode.OffGrid:
            battery_value.mod_r = 1
            battery_value.type = 2
        elif mode == BatteryMode.Charging:
            battery_value.mod_r = 1
            battery_value.type = 4
        else:
            raise UnknownBatteryMode

        return battery_value


class UnknownBatteryMode(Exception):
    """Error to indicate that battery mode in unknown."""
