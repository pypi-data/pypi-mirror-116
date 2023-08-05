from bscscan.enums.actions_enum import ActionsEnum as actions
from bscscan.enums.fields_enum import FieldsEnum as fields
from bscscan.enums.modules_enum import ModulesEnum as modules


class Stats:
    @staticmethod
    def get_total_bnb_supply():
        """Get total supply of BNB on Binance Smart Chain.

        Returns:
            str: The total supply of BNB.

        Example::

            from bscscan import BscScan

            async with BscScan(YOUR_API_KEY) as client:
                print(await client.get_total_bnb_supply())

        Results::

            "17673568869449800000000000"

        """
        return (
            f"{fields.MODULE}"
            f"{modules.STATS}"
            f"{fields.ACTION}"
            f"{actions.BNB_SUPPLY}"
        )

    @staticmethod
    def get_validators_list():
        """Get list of validators on Binance Smart Chain.

        Returns:
            List[dict]: All validators as a list of dictionaries.

        Example::

            from bscscan import BscScan

            async with BscScan(YOUR_API_KEY) as client:
                print(await client.get_validators_list())

        Results::

            [
                {
                    "validatorAddress": "0x9f8ccdafcc39f3c7d6ebf637c9151673cbc36b88",
                    "validatorName": "",
                    "validatorStatus": "0",
                    "validatorVotingPower": "43379676392570",
                    "validatorVotingPowerProportion": "0.0617"
                },
                {
                    "validatorAddress": "0x2465176c461afb316ebc773c61faee85a6515daa",
                    "validatorName": "",
                    "validatorStatus": "0",
                    "validatorVotingPower": "38039845465042",
                    "validatorVotingPowerProportion": "0.0541"
                },

                ...
            ]
        """
        return (
            f"{fields.MODULE}"
            f"{modules.STATS}"
            f"{fields.ACTION}"
            f"{actions.VALIDATORS}"
        )

    @staticmethod
    def get_bnb_last_price():
        """Get the last price of BNB against BTC and USD.

        Returns:
            dict: Latest dictionary of BNB price pairs.

        Example::

            from bscscan import BscScan

            async with BscScan(YOUR_API_KEY) as client:
                print(await client.get_bnb_last_price())


        Results::

            {
                "ethbtc": "0.00927",
                "ethbtc_timestamp": "1621600148",
                "ethusd": "379.15",
                "ethusd_timestamp": "1621600183"
            }
        """
        return (
            f"{fields.MODULE}"
            f"{modules.STATS}"
            f"{fields.ACTION}"
            f"{actions.BNB_PRICE}"
        )
