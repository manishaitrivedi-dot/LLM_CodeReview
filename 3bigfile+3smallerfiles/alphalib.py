from types import *
import numpy as np
from qubles.core.quble import Quble
from qubles.io.base.datalib import DataLib
from qubles.io.util.libaddress import LibAddress
from qubles.io.base.rootlib import RootLib
import qubles.core.functions.datetools as datetools 
 
# ===========================================  AlphaLib Class   ============================================

_PROPERTY_METADATA = {
    "fiscal_mode": {
        "display_name": "Fiscal Mode for Alpha Calculation",
        "default_value": "FY",
        "allowed_values": ["FY", "FQ", "FI", "FS"],
        "validators": ["non_null", "str"],
        "description": (
            "Default aggregation method for boolean data (used to indirectly set "
            "'aggr_method' via root_lazy_kwargs for bool Qubles)"
        ),
    },
    "lib_type": {
        "display_name": "Library Type",
        "default_value": "SFS_ALPHA",
        "allowed_values": ["SFS_ALPHA"],
        "validators": ["non_null", "str"],
        "description": ("Placeholder for property description"),
    },
    "prc_lib": {
        "display_name": "Process Library",
        "validators": ["non_null", "str"],
        "description": ("Placeholder for property description"),
    },
    "cft_lib": {
        "display_name": "Common Fundamental Template Library",
        "validators": ["non_null", "str"],
        "recording_flag": False,
        "description": ("Placeholder for property description"),
    },
    "est_summary_lib": {
        "display_name": "Estimated Summary Library",
        "validators": ["non_null", "str"],
        "description": ("Placeholder for property description"),
    },
    "index_price_field": {
        "display_name": "Index Price Field",
        "validators": ["non_null", "str"],
        "description": ("Placeholder for property description"),
    },
    "index_mktval_field": {
        "display_name": "Index Market Value Field",
        "validators": ["non_null", "str"],
        "description": ("Placeholder for property description"),
    },
    "industry_map": {
        "display_name": "Industry Map",
        "validators": ["non_null", "str"],
        "description": ("Placeholder for property description"),
    },
}


class AlphaLib(DataLib):
    fiscal_mode2ppy = {"FQ": 4, "FY": 1, "FS": 2, "FI": 4}

    periodicity2freq = {
        "CURRENT": None,
        "DAILY": "WEEKDAY",
        "WEEKLY": "W@FRI",
        "MONTHLY": "CEOM",
        "FQ": "CQ@MAR",
        "FS": "CS@JUN",
        "FY": "CA@DEC",
        "FI": "CA@DEC",
        "QUARTERLY": "CQ@MAR",
        "SEMI_ANNUALLY": "CS@JUN",
        "YEARLY": "CA@DEC",
    }
    periodicity2max_years = {
        "CURRENT": 1,
        "DAILY": 5,
        "WEEKLY": 15,
        "MONTHLY": 20,
        "FQ": 20,
        "QUARTERLY": 20,
        "FS": 20,
        "SEMI_ANNUALLY": 20,
        "FY": 20,
        "YEARLY": 20,
        "FI": 20,
        "INTERIM": 20,
    }

    periodicity2suffix = {
        "CURRENT": "_C",
        "DAILY": "_D",
        "WEEKLY": "_W",
        "MONTHLY": "_M",
        "FQ": "_FQ",
        "FS": "_FS",
        "FY": "_FY",
        "FI": "_FI",
        "QUARTERLY": "_Q",
        "SEMI_ANNUALLY": "_S",
        "YEARLY": "_Y",
    }
    freq2suffix = {
        "None": "_C",
        "WEEKDAY": "_D",
        "W@MON": "_W",
        "W@TUE": "_W",
        "W@WED": "_W",
        "W@THU": "_W",
        "W@FRI": "_W",
        "CEOM": "_M",
        "CQ@MAR": "_Q",
        "CS@JUN": "_S",
        "CA@DEC": "_Y",
    }

    lib_type2builder = {"SFS_ALPHA": None}

    def __init__(
        self,
        fields=None,
        default_properties=None,
        fldspec_properties=None,
        address=None,
        time_stamp="now",
        lib_type="SFS_ALPHA",
        **kwargs,
    ):
        """
        Alpha Factor Library

        lib_type
        --------
             'STD_ALPHA': Standard Alpha
        """
        # Establish non-trivial default_properties (if necessary)
        # ---------------------------------------------------------
        if default_properties is None:
            default_properties = {}

        # Augment default_properties arg w/kwargs
        # -------------------------------------------------------------------------
        # NOTE: Give deference to default_properties
        # [as to support persisted lib recovery which utilizes default_properties]
        # -------------------------------------------------------------------------
        for default_property_name, default_property_value in list(kwargs.items()):
            if default_property_name not in default_properties:
                default_properties[default_property_name] = default_property_value

        # Augment default_properties arg w/hardcoded defaults
        # -------------------------------------------------------------------------
        # NOTE: Give deference to default_properties
        # [as to support persisted lib recovery which utilizes default_properties]
        # -------------------------------------------------------------------------
        if "lib_type" not in default_properties:
            default_properties["lib_type"] = lib_type

        if default_properties["lib_type"] not in AlphaLib.lib_type2builder:
            raise Exception(
                f"Invalid lib_type assignment: {default_properties['lib_type']}"
            )
        default_properties["builder"] = AlphaLib.lib_type2builder[
            default_properties["lib_type"]
        ]

        if "field_category" not in default_properties:
            default_properties["field_category"] = "data"

        # """Consult QADDataLib & DataLib class constructor documentation"""
        super(AlphaLib, self).__init__(
            fields=fields,
            default_properties=default_properties,
            fldspec_properties=fldspec_properties,
            address=address,
            time_stamp=time_stamp,
        )
        return

    def initial_property_metadata(self):
        return self.merge_property_metadata(
            super(AlphaLib, self).initial_property_metadata(),
            _PROPERTY_METADATA,
        )

    def set_build_context(self, field):
        from qubles.io.base.rootlib import RootLib

        if (
            self.address is not None
            and self.address.base_domain
            and self.address.base_domain.is_root
        ):
            univ_address = RootLib().get_control("univ", grace=True)

            if univ_address is not None:
                if not isinstance(univ_address, LibAddress):
                    univ_address = LibAddress(univ_address)

                if self.address.append_subpath(field).globalize() == univ_address:
                    RootLib().set_control(
                        "univ", None, freeze_resolution="override"
                    )  # <-- Issuing override here

    # ======================================== UTILITIES =========================================

    def get_fiscal_field(
        self,
        field_prefix,
        fiscal_mode,
        lib,
        aggr_op1y=None,
        fiscal_keyspace="<fiscal_keyspace>",
        replace_missing_with_zero=False,
        ind_norm_op=None,
        aggr_op1y_ignore_missing=True,
        multi_year_window=None,
        multi_year_op=None,
        multi_year_pct_required=0.5,
        multi_year_ignore_missing=True,
        freq=None,
        add_frame=False,
        alt_field_prefix=None,
    ):
        """
        Retreives a fiscal field from the specified library

        field_prefix: prefix of the fiscal field to be retreived

        fiscal_mode: fiscal mode of the request
            'FQ': Quarterly Fiscal Context
            'FY': Yearly Fiscal Context
            'FS': Semi-Annual Fiscal Context
            'FI': Integrated (FQ/FS/FY) Fiscal Context

        lib: (String or DataLib) source library for the calendarized field request

        aggr_op1y: Time-Series Aggregation Operator to apply of trailing one

            Options: None, 'msum', 'mmean', 'mmedian', etc.

            fiscal_mode='FQ'/'FI': Apply time-series aggregation over trailing 4 fiscal quarters
            fiscal_mode='FS': Apply time-series aggregation over trailing 2 fiscal semi-annual periods
            fiscal_mode='FY': Already annualized, so do not need to apply aggr_op1y

        fiscal_mode: associated fiscal_keyspace for application of aggr_op1y
        replace_missing_with_zero: flag to replace missing values with zeros
        ind_norm_op: intra-industry normalization operation ('z', 'demean', etc)
        multi_year_window: Secondary post-processing window (expressed in years)
        multi_year_op: Secondary window operation (across fiscal time/space)
        multi_year_pct_required: non-missing percent of window required for multi year post-processing
        multi_year_ignore_missing: ignore_missing setting to be used for multi year post-processing
        freq: (calendarized) flag to perform calendarization (if requested, otherwise leave in fiscal time/space)
        add_frame: Flag to add_frame for safe allowance of control/environment changes (if necesssary)
            ==> Using default arg: add_frame=False (reduced overhead) with the presumption that this method
                will ONLY be called from within another method that has already provided a temporary frame setting]
        """
        # Establish lib
        # ---------------
        if lib is None:
            lib = self
        elif isinstance(lib, DataLib):
            pass
        elif isinstance(lib, str):
            lib = RootLib()[lib]
        else:
            raise Exception(f"Invalid lib:{lib}...String or DataLib expected")

        if not isinstance(lib, DataLib):
            raise Exception("Unable to resolve lib arg to a DataLib")

        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]

        # Establish field name
        # -----------------------
        if (
            field_prefix is None
            or not isinstance(field_prefix, str)
            or len(field_prefix) == 0
        ):
            raise Exception(f"Invalid field_prefix:{field_prefix}")

        elif fiscal_mode not in ("FQ", "FI", "FS", "FY"):
            raise Exception(f"Invalid fiscal_mode:{fiscal_mode}")

        else:
            field = f"{field_prefix}_{fiscal_mode}"

        # Investigate need to substitute alt_field_prefix (if applicable)
        # [In this scenario, primary field is not available within the specified lib,
        #  but the user provided secondary/alternate field prefix (alt_field_prefix)]
        # --------------------------------------------------------------------------
        if alt_field_prefix is not None and field not in lib.fields():
            if (
                alt_field_prefix is None
                or not isinstance(alt_field_prefix, str)
                or len(alt_field_prefix) == 0
            ):
                raise Exception(f"Invalid alt_field_prefix:{alt_field_prefix}")
            field_prefix = alt_field_prefix
            field = f"{field_prefix}_{fiscal_mode}"

        # Perform initial request
        # ---------------------------
        result = lib[field]
        if result is None:
            return result

        if replace_missing_with_zero:
            result[result.where_missing()] = 0.0

        # Add a temporary frame (if instructed)
        if add_frame:
            RootLib().add_frame()

        # ================================================================
        # If applicable, Apply Trailing 1 Year Aggregation (aggr_op1y)
        # ================================================================
        if aggr_op1y is None:
            pass

        # Fiscal Yearly Case (FY)
        # ---------------------------
        elif fiscal_mode == "FY":
            # For fiscal_mode 'FY' (annual mode): Some aggr_op1y can be applied for periods=1
            if aggr_op1y in ("mdiff", "diff", "mpctchg", "pctchg", "shift"):
                if fiscal_keyspace is None or fiscal_keyspace == "<fiscal_keyspace>":
                    fiscal_keyspace = self.get_property(
                        "fiscal_keyspace", grace=False
                    )  # <-- Not field specific

                if aggr_op1y in ("mdiff", "diff"):
                    # For Quble class, aggr_method='diff' not supported through generic maggregate1d method
                    # pct_required not applicable here for Quble
                    result = result.mdiff1d(
                        periods=1, keyspace=fiscal_keyspace, ignore_add=False
                    )
                elif aggr_op1y in ("mpctchg", "pctchg"):
                    # For Quble class, aggr_method='pctchg' not supported through generic maggregate1d method
                    # pct_required not applicable here for Quble
                    result = result.mpctchg1d(
                        periods=1,
                        keyspace=fiscal_keyspace,
                        ignore_mult=False,
                        ignore_add=False,
                    )
                else:
                    # Note: Using ignore_missing=False for periods=1
                    result = result.shift1d(periods=1, keyspace=fiscal_keyspace)

            elif aggr_op1y in ("mstd", "std", "absdev", "mabsdev"):
                raise Exception(
                    "fiscal_mode:{0}...application of maggregate:{1} requires window size > 1".format(
                        fiscal_mode, aggr_op1y
                    )
                )

            # For fiscal_mode 'FY' (annual mode w/periods=1): many aggr_op1y
            # (e.g., 'sum','mean','median',etc.) simply yield the annual fiscal data
            elif aggr_op1y in (
                "mmean",
                "mave",
                "msum",
                "mmedian",
                "mmin",
                "mmax",
                "mprod",
                "mvar",
                "mstd",
                "mskew",
                "mkurtosis",
                "mean",
                "ave",
                "sum",
                "median",
                "min",
                "max",
                "prod",
                "var",
                "std",
                "skew",
                "kurtosis",
            ):
                pass  # <-- For these operators when window=1...no operation/transform needed

            # Trying to be careful here so as not to simply pass through raw data without proper consideration
            else:
                raise Exception(
                    f"fiscal_mode:{fiscal_mode}...Unexpected maggregate:{aggr_op1y}"
                )

        # Fiscal Quarterly, Semi-Annual & Integrate Cases (FQ/FS/FI)
        # -------------------------------------------------------------
        elif fiscal_mode in ("FQ", "FI", "FS"):
            if fiscal_keyspace is None or fiscal_keyspace == "<fiscal_keyspace>":
                fiscal_keyspace = self.get_property(
                    "fiscal_keyspace", grace=False
                )  # <-- Not field specific

            if aggr_op1y in ("mabsdev", "absdev"):
                RootLib().set_control("ignore_mult", False)
                RootLib().set_control("ignore_add", False)
                meanN = result.mmean1d(
                    periods=fiscal_ppy,
                    keyspace=fiscal_keyspace,
                    pct_required=1.0,
                    ignore_missing=aggr_op1y_ignore_missing,
                )
                abs_devs = (result - meanN).absolute()
                mean_abs_devs = abs_devs.mmean1d(
                    periods=fiscal_ppy,
                    keyspace=fiscal_keyspace,
                    pct_required=1.0,
                    ignore_missing=aggr_op1y_ignore_missing,
                )
                result = mean_abs_devs / meanN

            elif aggr_op1y in ("mdiff", "diff"):
                # For Quble class, aggr_method='mdiff' not supported through generic maggregate1d method
                # pct_required not applicable here for Quble
                result = result.mdiff1d(
                    periods=fiscal_ppy, keyspace=fiscal_keyspace, ignore_add=False
                )
            elif aggr_op1y in ("mpctchg", "pctchg"):
                # For Quble class, aggr_method='mpctchg' not supported through generic maggregate1d method
                # pct_required not applicable here for Quble
                result = result.mpctchg1d(
                    periods=fiscal_ppy,
                    keyspace=fiscal_keyspace,
                    ignore_mult=False,
                    ignore_add=False,
                )
            elif aggr_op1y == "shift":
                result = result.shift1d(periods=fiscal_ppy, keyspace=fiscal_keyspace)

            else:
                # Here, we call maggregate1d() method
                # with the appropriate aggr_method arg
                if aggr_op1y in (
                    "mean",
                    "ave",
                    "sum",
                    "median",
                    "min",
                    "max",
                    "prod",
                    "var",
                    "std",
                    "skew",
                    "kurtosis",
                ):
                    aggr_op1y = f"m{aggr_op1y}"

                result = result.maggregate1d(
                    periods=fiscal_ppy,
                    keyspace=fiscal_keyspace,
                    pct_required=0.74,
                    aggr_method=aggr_op1y,
                    ignore_missing=aggr_op1y_ignore_missing,
                )
        else:
            raise Exception(f"Invalid fiscal_mode:{fiscal_mode}")

        # Apply (cross-sectional) intra-industry normalization (if applicable)
        # ---------------------------------------------------------------------
        if ind_norm_op is not None:
            result = self.industry_normalization(result, norm_op=ind_norm_op)

        # Apply (secondary/post-processing) multi-year moving aggregation (if required)
        # -------------------------------------------------------------------------------
        if multi_year_window is not None and multi_year_op is not None:
            if fiscal_keyspace is None or fiscal_keyspace == "<fiscal_keyspace>":
                fiscal_keyspace = self.get_property(
                    "fiscal_keyspace", grace=False
                )  # <-- Not field specific

            # Note: Need to use fiscal_ppy here as the multi_year_window is (intentionally) provided in years (not periods)
            # For example, when multi_year_window=5 (years) and (Fiscal Quarterly) fiscal_mode='FQ' (fiscal_ppy=4),
            # we need to perform the aggregation over (4*5)=20 Quarters
            # ------------------------------------------------------------------------------
            if multi_year_op in ("mabsdev", "absdev"):
                src_meanN = result.mmean1d(
                    (fiscal_ppy * multi_year_window),
                    keyspace=fiscal_keyspace,
                    pct_required=1.0,
                    ignore_missing=True,
                )
                src_abs_devs = (result - src_meanN).absolute()
                src_mean_abs_devs = src_abs_devs.mmean1d(
                    (fiscal_ppy * multi_year_window),
                    keyspace=fiscal_keyspace,
                    pct_required=1.0,
                    ignore_missing=True,
                )
                result = src_mean_abs_devs / src_meanN

            elif multi_year_op in ("mpctchg", "pctchg"):
                # For Quble class, aggr_method='mpctchg' not supported through generic maggregate1d method
                # pct_required not applicable here for Quble
                result = result.mpctchg1d(
                    periods=(fiscal_ppy * multi_year_window),
                    keyspace=fiscal_keyspace,
                    ignore_mult=False,
                    ignore_add=False,
                )
            else:
                result = result.maggregate1d(
                    periods=(fiscal_ppy * multi_year_window),
                    keyspace=fiscal_keyspace,
                    pct_required=multi_year_pct_required,
                    aggr_method=multi_year_op,
                    ignore_missing=multi_year_ignore_missing,
                )

        # Calendar the result (if applicable)
        if freq is not None:
            result = self.calendarize(result, freq=freq, add_frame=False)

        # Pop the temporary frame (if applicable)
        if add_frame:
            RootLib().pop_frame()

        return result

    def get_fiscal_unexp(
        self,
        src_field_prefix,
        scale_field_prefix,
        denom_field_prefix,
        fiscal_mode,
        lib,
        freq=None,
        src_aggr_op1y=None,
        scale_aggr_op1y="msum",
        denom_aggr_op1y=None,
        fiscal_keyspace="<fiscal_keyspace>",
        add_frame=False,
        **kwds_args,
    ):
        """
        Returns the 'unexpected' data/version of a field using scaling & normalization:

        fiscal_mode='FQ': unexp[Q] = ( <src>_FQ[Q] - (<src>_FQ[Q-4] * (MSUM( <scale>_FQ[Q], 4) / MSUM(scale,4))[Y-4])) / <denom>_FQ[Q-4]
        fiscal_mode='FY': unexp[Y] = ( <src>_FY[Y] - (<src>_FY[Y-1] * (<scale>_FY[Y] / <scale>_FY[Y-1]))) / <denom>_FY[Y-1]
        fiscal_mode='FS': unexp[S] = ( <src>_FS[S] - (<src>_FS[S-2] * (MSUM(<scale>_FS[S],2) / MSUM(<scale>_FS,2))[S-4])) / <denom>_FS[S-2]

        Here the scale time-series data is providing a reference as to an expected value (trajectory) of src time-series data
        Returns a normalized version of the deviation (difference) from this expected/implied value

        Requires that src & scale & denom fields are all procured from the same (fiscal) lib

        freq: (calendarized) freq (if requested, otherwise leave in fiscal time/space)
        add_frame: Flag to add_frame for safe allowance of control/environment changes (if necesssary)
            ==> Using default arg: add_frame=False (reduced overhead) with the presumption that this method
                will ONLY be called from within another method that has already provided a temporary frame setting]
        """
        # Validate inputs
        if src_field_prefix is None:
            raise Exception(f"Bad src_field_prefix: {src_field_prefix}")

        elif scale_field_prefix not in ("SALES", "PPE_GROSS", "COGS"):
            raise Exception(f"Bad scale_field_prefix: {scale_field_prefix}")

        elif denom_field_prefix not in ("ASSETS"):
            raise Exception(f"Bad denom_field_prefix: {denom_field_prefix}")

        # Procure fiscal_keyspace (for shift1D calls below)
        if fiscal_keyspace is None or fiscal_keyspace == "<fiscal_keyspace>":
            fiscal_keyspace = self.get_property(
                "fiscal_keyspace", grace=True, default_property_value="Fiscal"
            )

        if add_frame:
            RootLib().add_frame()

        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        # Procure src data
        src = self.get_fiscal_field(
            src_field_prefix,
            fiscal_mode,
            lib,
            aggr_op1y=src_aggr_op1y,
            fiscal_keyspace=fiscal_keyspace,
            freq=None,
        )
        src_lag1y = src.shift1d(fiscal_ppy, keyspace=fiscal_keyspace)

        # Procure scale data [Note use of 'msum' in default arg above here]
        scale = self.get_fiscal_field(
            src_field_prefix,
            fiscal_mode,
            lib,
            aggr_op1y=scale_aggr_op1y,
            fiscal_keyspace=fiscal_keyspace,
            freq=None,
        )
        scale_lag1y = scale.shift1d(fiscal_ppy, keyspace=fiscal_keyspace)

        # Procure denom data
        denom = self.get_fiscal_field(
            src_field_prefix,
            fiscal_mode,
            lib,
            aggr_op1y=denom_aggr_op1y,
            fiscal_keyspace=fiscal_keyspace,
            freq=None,
        )
        denom_lag1y = denom.shift1d(fiscal_ppy, keyspace=fiscal_keyspace)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        result = (src - (src_lag1y * (scale / scale_lag1y))) / denom_lag1y

        if freq is not None:
            result = self.calendarize(result, freq=freq, add_frame=False)

        if add_frame:
            RootLib().pop_frame()

        return result

    def get_calendarized_field(
        self,
        field_prefix,
        freq,
        lib,
        tfill_method_dict=None,
        tfill_max_dict=None,
        ind_norm_op=None,
    ):
        """
        Retreives a calendarized field from the specified library

        field_prefix: prefix of the calendarized field to be retreived
        freq: Frequency of the calendarized field to the retrieved
              ==> freq will be used to assign an approriate calendarized suffix to the field_prefix
        lib: (String or DataLib) source library for the calendarized field request
        tfill_method_dict: tfill_method by freq (if/when applicable)
        tfill_max_dict: tfill_max by freq (if/when applicable)
        ind_norm_op: intra-industry normalization operation ('z', 'demean', etc)
        """
        # Establish lib
        # ---------------
        if lib is None:
            lib = self
        elif isinstance(lib, DataLib):
            pass
        elif isinstance(lib, str):
            lib = RootLib()[lib]
        else:
            raise Exception(f"Invalid lib:{lib}...String or DataLib expected")

        if not isinstance(lib, DataLib):
            raise Exception("Unable to resolve lib arg to a DataLib")

        # Establish fiscal field name
        # ------------------------------
        if (
            field_prefix is None
            or not isinstance(field_prefix, str)
            or len(field_prefix) == 0
        ):
            raise Exception(f"Invalid field_prefix:{field_prefix}")

        elif freq not in AlphaLib.freq2suffix:
            raise Exception(f"Invalid freq:{freq}")

        else:
            field = field_prefix + AlphaLib.freq2suffix[freq]

        # Access the calendarized field
        # -------------------------------
        result = lib[field]

        # Perform Fill (if applicable)
        # ------------------------------
        if (
            tfill_method_dict is not None
            and freq in tfill_method_dict
            and tfill_method_dict[freq] is not None
        ):
            tfill_method = tfill_method_dict[freq]
            if (
                tfill_max_dict is not None
                and freq in tfill_max_dict
                and tfill_max_dict[freq] is not None
            ):
                tfill_max = tfill_max_dict[freq]
            else:
                tfill_max = None

            dates_keyspace = lib.get_property("dates_keyspace", grace=False)
            result = result.fill1d(
                keyspace=dates_keyspace, tfill_method=tfill_method, tfill_max=tfill_max
            )

        return (
            result
            if ind_norm_op is None
            else self.industry_normalization(result, norm_op=ind_norm_op)
        )

    def calendarize(
        self,
        fiscal_data,
        fiscal_keyspace="<fiscal_keyspace>",
        dates_keyspace="<dates_keyspace>",
        freq="<freq>",
        add_frame=False,
    ):
        """
        Calendarizes a fiscal data object
        fiscal_data: the fiscal-based data to be calendarized
        fiscal_keyspace: the fiscal time keyspace to be translated from
        dates_keyspace: the calendar time keyspace to be translated to
        add_frame: Flag to add_frame for safe allowance of control/environment changes (if necesssary)
            ==> Using default arg: add_frame=False (reduced overhead) with the presumption that this method
                will ONLY be called from within another method that has already provided a temporary frame setting]
        """
        if add_frame:
            RootLib().add_frame()

        if fiscal_keyspace is None or fiscal_keyspace == "<fiscal_keyspace>":
            fiscal_keyspace = self.get_property(
                "fiscal_keyspace", grace=False
            )  # <-- Not field specific

        if dates_keyspace is None or dates_keyspace == "<dates_keyspace>":
            dates_keyspace = self.get_property(
                "dates_keyspace", grace=False
            )  # <-- Not field specific

        if freq is None or freq == "<freq>":
            freq = RootLib().get_control('freq')
        else:
            RootLib().set_control("freq", freq)

        # Configure (temporary) RootLib/environment to use desired (calendar) freq map
        # when converting from fiscal -> calendar-time below
        calendar_data = RootLib().remap(
            fiscal_data, src_keyspaces=fiscal_keyspace, tgt_keyspaces=dates_keyspace
        )

        # Apply time filling when applicable
        if isinstance(calendar_data, Quble) and calendar_data.is_defined:
            first_time_keyspace = calendar_data.first_time_keyspace()
            tfill_max_dict = {}
            if first_time_keyspace:
                for vs in calendar_data.valuespaces:
                    tfill_max = calendar_data.get_space_info(
                        space=vs, info_type="tfill_max"
                    )
                    tfill_max_dict[vs] = tfill_max
                    # Think about tfill_honor_nulls setting
            calendar_data = calendar_data.fill1d(
                keyspace=first_time_keyspace,
                valuespace=calendar_data.valuespaces,
                tfill_method="pad",
                tfill_max=tfill_max_dict,
                tfill_end_mode="no_future",
                tfill_honor_nulls=True,
            )

        if add_frame:
            RootLib().pop_frame()
        return calendar_data

    def industry_normalization(
        self, raw_quble, norm_op, industry_map=None, **kwds_args
    ):
        if industry_map is None:
            industry_map = self.get_property("industry_map", grace=False)

        if isinstance(industry_map, str):
            industry_map = RootLib()[industry_map]

        if not isinstance(industry_map, (Quble)):
            raise Exception(f"Invalid industry_map:{industry_map}")

        # Apply normalization as directed
        # ----------------------------------
        if norm_op == "demean":
            # <-- tgt_keyspace arg is arbitrary here when unmap_flag=True
            return raw_quble.sub_mean1d(
                keymap=industry_map,
                keyspace="SECMSTR",
                tgt_keyspace="industries",
                ignore_missing=True,
                link_check=False,
                unmap_flag=True,
            )
        elif norm_op == "z":
            return raw_quble.sub_zscore1d(
                keymap=industry_map,
                keyspace="SECMSTR",
                ignore_missing=True,
                link_check=False,
            )

        else:
            raise Exception(f"Invalid norm_op:{norm_op}")

    # ===================================== NON-ALPHA / HELPER FACTORS =======================================

    @RootLib.temp_frame()
    def EV(self, field, **kwds_args):
        """Enterprise Value = MKT_VAL + LTD + CURR_LTD - CASH"""

        # Get Properties
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)

        # Evaluate fiscal_mode & freq here (not in get_fiscal_field() method) as we want to allow for field-specific use
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=prc_lib)

        ltd = self.get_fiscal_field(
            field_prefix="LTD", fiscal_mode=fiscal_mode, lib=cft_lib, freq=None
        )
        curr_ltd = self.get_fiscal_field(
            "CURR_LTD", fiscal_mode=fiscal_mode, lib=cft_lib, freq=None
        )
        cash = self.get_fiscal_field(
            field_prefix="CASH", fiscal_mode=fiscal_mode, lib=cft_lib, freq=None
        )

        RootLib().set_control("ignore_add", "right")
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        debt_items = ltd + curr_ltd - cash  # <-- In fiscal time/space
        if freq is not None:
            debt_items = self.calendarize(debt_items, freq=freq, add_frame=False)
        ev = mv + debt_items
        return ev

    @RootLib.temp_frame()
    def IC(self, field, **kwds_args):
        """Invested Capital = LTD + CURR_LTD + TOT_PREF_STK + MINOR_INT_LIAB + TOT_COM_STK"""
        # DL:IC_FQ = (LTD_FQ + CURR_LTD_FQ + TOT_PREF_STK_FQ + MINOR_INT_LIAB_FQ + TOT_COM_STK_FQ)

        # Get Properties
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        ltd = self.get_fiscal_field(
            field_prefix="LTD", fiscal_mode=fiscal_mode, lib=cft_lib, freq=None
        )
        curr_ltd = self.get_fiscal_field(
            field_prefix="CURR_LTD", fiscal_mode=fiscal_mode, lib=cft_lib, freq=None
        )
        pref_stk = self.get_fiscal_field(
            field_prefix="TOT_PREF_STK", fiscal_mode=fiscal_mode, lib=cft_lib, freq=None
        )
        minor_int_liab = self.get_fiscal_field(
            field_prefix="MINOR_INT_LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            freq=None,
        )
        common_stk = self.get_fiscal_field(
            field_prefix="TOT_COM_STK", fiscal_mode=fiscal_mode, lib=cft_lib, freq=None
        )

        RootLib().set_control("ignore_add", True)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        ic_fiscal = ltd + curr_ltd + pref_stk + minor_int_liab + common_stk
        return (
            self.calendarize(ic_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else ic_fiscal
        )

    @RootLib.temp_frame()
    def NOA(self, field, **kwds_args):
        """Net Operating Assets = [Op Assets - Op Liab] = [(Total Assets - Cash) - (Total Liab - LTD - Curr Portion of LTD)]
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR!!!"""

        # Get Properties
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Perform computations
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        liab = self.get_fiscal_field(
            field_prefix="LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        ltd = self.get_fiscal_field(
            field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_ltd = self.get_fiscal_field(
            field_prefix="CURR_LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- Will Required Non-Missing assets & liab
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        noa_fiscal = (assets - cash) - (liab - ltd - curr_ltd)
        return (
            self.calendarize(noa_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else noa_fiscal
        )

    @RootLib.temp_frame()
    def NET_ASSETS(self, field, **kwds_args):
        """Net Assets"""
        # DL:NET_ASSETS_FQ = (CASH_FQ + PPE_NET_FQ + WC_FQ)
        # DL:NET_ASSETS_FQ = (CASH_FQ + PPE_NET_FQ + (RECEIVABLES_FQ + INVENTORY_FQ - PAYABLES_FQ))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        ppe_net = self.get_fiscal_field(
            field_prefix="PPE_NET",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        wc = self.get_fiscal_field(
            field_prefix="WC",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_add", True)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        net_assets_fiscal = cash + ppe_net + wc
        return (
            self.calendarize(net_assets_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else net_assets_fiscal
        )

    # ======================================== VALUATION FACTORS =========================================

    @RootLib.temp_frame()
    def SALES2P(self, field, **kwds_args):
        """SALES2P: Sales / MKTCAP (Rolling 4 Quarters)"""
        # FL:SALES2P = MSUM(SALES_FQ,4) / MKT_VAL
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=freq,
        )  # <-- Convert to calendar time/space
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=prc_lib)
        return sales_sum1y / mv

    @RootLib.temp_frame()
    def E2P(self, field, **kwds_args):
        """E2P: Net Income Before XO Items (Basic) / MKTCAP (Rolling 4 Quarters)"""
        # FL:E2P = MSUM(NI_COMMON_FQ,4) / MKT_VAL
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)

        # Evaluate fiscal_mode & freq here (not in get_fiscal_field() method) as we want to allow for field-specific use
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        net_income_common_sum1y = self.get_fiscal_field(
            field_prefix="NI_COMMON_B4X",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=freq,
        )  # <-- Convert to calendar time/space
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=prc_lib)
        return net_income_common_sum1y / mv

    @RootLib.temp_frame()
    def CF2P(self, field, **kwds_args):
        """CF2P: Cash Flow / MKTCAP (Rolling 4 Quarters)"""
        # FL:CF2P = MSUM(CF_FQ,4) / MKT_VAL
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)

        # Evaluate fiscal_mode & freq here (not in get_fiscal_field() method) as we want to allow for field-specific use
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        cf_sum1y = self.get_fiscal_field(
            field_prefix="CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=freq,
        )  # <-- Convert to calendar time/space
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=prc_lib)
        return cf_sum1y / mv

    @RootLib.temp_frame()
    def FCF2P(self, field, **kwds_args):
        """FCF2P: Free Cash Flow / MKTCAP (Rolling 4 Quarters)"""
        # FL:FCF2P = MSUM(FCF_FQ,4) / MKT_VAL
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)

        # Evaluate fiscal_mode & freq here (not in get_fiscal_field() method) as we want to allow for field-specific use
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        fcf_sum1y = self.get_fiscal_field(
            field_prefix="FCF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=freq,
        )  # <-- Convert to calendar time/space
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=prc_lib)
        return fcf_sum1y / mv

    @RootLib.temp_frame()
    def D2P(self, field, **kwds_args):
        """D2P: Dividends / MKTCAP (Rolling 4 Quarters)"""
        # FL:D2P (aka DIVIDEND YIELD) = [MSUM(-1.*CASHDIV_PD_CF_FQ,4) / MKT_VAL]     NOTE: (CASHDIV_PD_CF_FQ < 0)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)

        # Evaluate fiscal_mode & freq here (not in get_fiscal_field() method) as we want to allow for field-specific use
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        # NOTE: (CASHDIV_PD_CF_FQ/FI/FS/FY < 0)
        cash_divs_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CASHDIV_PD_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=freq,
        )  # <-- Convert to calendar time/space
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=prc_lib)
        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        return cash_divs_sum1y / mv

    @RootLib.temp_frame()
    def ID2P(self, field, **kwds_args):
        """ID2P: (Indicated Dividends) / MKTCAP (Rolling 4 Quarters)"""
        # FL:ID2P (aka INDICATED DIVIDEND YIELD) = [(4 * Q2D(-1.*CASHDIV_PD_CF_FQ)) / MKT_VAL]    NOTE: (CASHDIV_PD_CF_FQ < 0)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        annualizer_dict = {"FQ": 4.0, "FI": 4.0, "FS": 2.0, "FY": 1.0}
        # NOTE: (CASHDIV_PD_CF_FQ/FI/FS/FY < 0)
        cash_idivs = (
            -1.0
            * annualizer_dict[fiscal_mode]
            * self.get_fiscal_field(
                field_prefix="CASHDIV_PD_CF",
                fiscal_mode=fiscal_mode,
                lib=cft_lib,
                aggr_op1y=None,
                freq=freq,
            )
        )  # <-- Convert to calendar time/space
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=prc_lib)

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        return cash_idivs / mv

    @RootLib.temp_frame()
    def B2P(self, field, **kwds_args):
        """B2P: Equity / MKTCAP (Rolling 4 Quarters)"""
        # FL:B2P (aka BOOK YIELD) = MSUM(EQUITY_FQ,4) / MKT_VAL
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        equity = self.get_fiscal_field(
            field_prefix="EQUITY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=freq,
        )  # <-- Convert to calendar time/space
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=prc_lib)
        return equity / mv

    @RootLib.temp_frame()
    def SALES2EV(self, field, **kwds_args):
        """SALES2EV: Sales / EV (Rolling 4 Quarters)"""
        # FL:SALES2EV = Q2D(MSUM(SALES_FQ,4)) / EV
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=freq,
        )  # <-- Convert to calendar time/space
        ev = self.get_calendarized_field(field_prefix="EV", freq=freq, lib=self)
        return sales_sum1y / ev

    @RootLib.temp_frame()
    def GP2EV(self, field, **kwds_args):
        """GP2EV: GP / EV (Rolling 4 Quarters)"""
        # FL:GP2EV = Q2D(MSUM(GP_FQ,4)) / EV
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        gp_sum1y = self.get_fiscal_field(
            field_prefix="GP",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=freq,
        )  # <-- Convert to calendar time/space
        ev = self.get_calendarized_field(field_prefix="EV", freq=freq, lib=self)
        return gp_sum1y / ev

    @RootLib.temp_frame()
    def EBITDA2EV(self, field, **kwds_args):
        """EBITDA2EV: EBITDA / EV (Rolling 4 Quarters)"""
        # FL:EBITDA2EV = Q2D(MSUM(EBITDA_FQ,4)) / EV
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        ebitda_sum1y = self.get_fiscal_field(
            field_prefix="EBITDA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=freq,
        )  # <-- Convert to calendar time/space
        ev = self.get_calendarized_field(field_prefix="EV", freq=freq, lib=self)
        return ebitda_sum1y / ev

    @RootLib.temp_frame()
    def EBIT2EV(self, field, **kwds_args):
        """EBIT2EV: EBITDA / EV (Rolling 4 Quarters)"""
        # FL:EBIT2EV = Q2D(MSUM(EBIT_FQ,4)) / EV
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        ebit = self.get_fiscal_field(
            field_prefix="EBIT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=freq,
        )  # <-- Convert to calendar time/space
        ev = self.get_calendarized_field(field_prefix="EV", freq=freq, lib=self)
        return ebit / ev

    @RootLib.temp_frame()
    def IC2EV(self, field, **kwds_args):
        """IC2EV: IC / EV = Invested Capital / Enterprise Value
        See" 'The Productivity Premium in Equity Returns' by Brown & Row (2005)"""
        # FL:IC2EV = Q2D(IC_FQ)/EV
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        ic_fiscal = self.get_fiscal_field(
            field_prefix="IC", fiscal_mode=fiscal_mode, lib=self, freq=freq
        )  # <-- Convert to calendar time/space
        ev = self.get_calendarized_field(field_prefix="EV", freq=freq, lib=self)
        return ic_fiscal / ev

    @RootLib.temp_frame()
    def PAYOUT(self, field, **kwds_args):
        """PAYOUT_FQ: Dividend Payout Ratio = MSUM(Cash Dividends,4) / MSUM(NI Before Extras,4) (Rolling 4 Qtrs)"""
        # FL:PAYOUT_FQ = MSUM(-1.*CASHDIV_PD_CF_FQ,4) / MSUM(NIB4X_FQ,4)   NOTE: (CASHDIV_PD_CF_FQ < 0)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        nib4extras_sum1y = self.get_fiscal_field(
            field_prefix="NIB4X",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # Require non-negative nib4extras
        nib4extras_sum1y.conditional_nullify_inplace(nib4extras_sum1y < 0)

        cash_divs_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CASHDIV_PD_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        payout_fiscal = cash_divs_sum1y / nib4extras_sum1y
        RootLib().set_control("ignore_mult", False)
        return (
            self.calendarize(payout_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else payout_fiscal
        )

    @RootLib.temp_frame()
    def ASSETS2EV(self, field, **kwds_args):
        """ASSETS2EV: Assets / EV"""
        # FL:ASSETS2EV = ASSETS / EV
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=freq,
        )  # <-- Convert to calendar time/space
        ev = self.get_calendarized_field(field_prefix="EV", freq=freq, lib=self)
        return assets / ev

    @RootLib.temp_frame()
    def TOBIN_QRATIO(self, field, **kwds_args):
        """TOBIN_QRATIO: Tobin's Q-Ratio (Replacement Value)"""
        #  FL:TOBIN_QRATIO = (MKTCAP + LIAB) / ASSETS
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)

        # Evaluate fiscal_mode & freq here (not in get_fiscal_field() method) as we want to allow for field-specific use
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        liab = self.get_fiscal_field(
            field_prefix="LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=prc_lib)

        # Set 'ignore_add' to 'right' so that we REQUIRE a non-missing mv records in tobin_qratio expression below
        RootLib().set_control("ignore_add", "right")
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        tobin_qratio = (mv + liab) / assets

        return tobin_qratio

    # Note: Need to use temp_frame decorator here as this method may be called as a field builder in some scenarios
    @RootLib.temp_frame()
    def EST_FWD1Y(
        self,
        field,
        freq=None,
        est_category_name=None,
        est_stats_name=None,
        est_summary_lib=None,
        est_dates_keyspace=None,
        **kwds_args,
    ):
        """Examples: self.EST_FWD1Y(field='FWD_EPS_M', freq='CEOM', est_category_name='EPS', est_stats_name='MEAN')
        self.EST_FWD1Y(field='FWD_REV_M', freq='CEOM', est_category_name='REV', est_stats_name='MEDIAN')
        """

        if freq is None:
            freq = self.get_property(
                "freq", field, grace=True, resolve_templates=True
            )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        if freq not in AlphaLib.freq2suffix:
            raise Exception(f"Invalid freq:{freq}")

        if est_category_name is None:
            est_category_name = self.get_property(
                "est_category_name", field, grace=False
            )

        if est_stats_name is None:
            est_stats_name = self.get_property(
                "est_stats_name", field, grace=True, default_property_value="MEAN"
            )

        if est_summary_lib is None:
            est_summary_lib = self.get_property(
                "est_summary_lib",
                field,
                grace=True,
                default_property_value="IBES2 Summary",
            )

        if est_dates_keyspace is None:
            est_dates_keyspace = RootLib()[est_summary_lib].get_property(
                "dates_keyspace", grace=False
            )

        # Procure FY1 Information
        # --------------------------
        est_data_field_fy1 = (
            f"{est_category_name}_FY1_{est_stats_name}{AlphaLib.freq2suffix[freq]}"
        )
        est_repdate_field_fy1 = (
            f"{est_category_name}_FY1_REPDATE{AlphaLib.freq2suffix[freq]}"
        )

        est_data_fy1 = RootLib()[est_summary_lib][est_data_field_fy1]
        est_repdate_fy1 = RootLib()[est_summary_lib][est_repdate_field_fy1]
        est_countdown_fy1 = est_repdate_fy1.countdown_days(keyspace=est_dates_keyspace)

        # Procure FY2 Information
        # --------------------------
        est_data_field_fy2 = (
            f"{est_category_name}_FY2_{est_stats_name}{AlphaLib.freq2suffix[freq]}"
        )
        est_repdate_field_fy2 = (
            f"{est_category_name}_FY2_REPDATE{AlphaLib.freq2suffix[freq]}"
        )

        est_data_fy2 = RootLib()[est_summary_lib][est_data_field_fy2]

        # Assign enviroment settings

        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        if est_data_fy1.is_undefined:
            if est_data_fy2.is_undefined:
                return est_data_fy1.copy()  # arbitrary
            else:
                return est_data_fy2.copy()
        elif est_data_fy2.is_undefined:
            return est_data_fy1.copy()
        elif est_data_fy1.is_nonvariate:
            raise Exception("est_data_fy1 (Quble) is non-variate")
        elif est_data_fy2.is_nonvariate:
            raise Exception("est_data_fy2 (Quble) is non-variate")
        else:
            # Here, both est_data_fy1 & est_data_fy2 are defined, variate Qubles

            # Build the multi-variate computation Quble
            data = Quble.undefined_instance()
            RootLib().set_control("keys_join_op", "union")
            data["est_data_fy1"] = est_data_fy1.convert_fx(None, grace=True)
            data["est_data_fy2"] = est_data_fy2.convert_fx(None, grace=True)
            data["countdown_pct1"] = (
                est_countdown_fy1.change_dtype(float) / 365.25
            )  # <-- Countdown is provided in # CALENDAR Days (1.0/365.25) = 0.0027378507871321013
            # data['countdown_pct2'] = est_countdown_fy2.change_dtype(float)/365.25 # <-- Countdown is provided in # CALENDAR Days (1.0/365.25) = 0.0027378507871321013
            data["fy1_not_missing"] = (
                data["est_data_fy1"].where_not_missing()
                & data["countdown_pct1"].where_not_missing()
            )
            # data['fy2_not_missing'] = (data['est_data_fy2'].where_not_missing() & data['countdown_pct2'].where_not_missing())
            data["fy2_not_missing"] = data["est_data_fy2"].where_not_missing()
            data["both_not_missing"] = data["fy1_not_missing"] & data["fy2_not_missing"]
            data["only_fy1_not_missing"] = data["fy1_not_missing"] & (
                data["fy2_not_missing"] != True
            )
            data["only_fy2_not_missing"] = data["fy2_not_missing"] & (
                data["fy1_not_missing"] != True
            )

            # First, limit to 'both_not_missing'
            fy1_wt = data["countdown_pct1"].conditional_keep(data["both_not_missing"])
            fy1_wt[fy1_wt > 1.0] = 1.0  # <-- Just to be safe!!
            fy1_wt[fy1_wt < 0.0] = 0.0  # <-- Just to be safe!!

            fy2_wt = 1.0 - fy1_wt

            # Now expand to only fy1 or only fy2 missing
            fy1_wt[data["only_fy1_not_missing"]] = 1.0
            fy2_wt[data["only_fy2_not_missing"]] = 1.0

            # Assign fy1 & fy2 weights to computational Quble
            data["fy1_wt"] = fy1_wt
            data["fy2_wt"] = fy2_wt

            # Perform weighted average computation
            data_wtdave = (
                (data["fy1_wt"] * data["est_data_fy1"])
                + (data["fy2_wt"] * data["est_data_fy2"])
            ) / (
                data["fy1_wt"] + data["fy2_wt"]
            )  # <-- Should not need the denominator here, but trying to be safe

            return data_wtdave

    @RootLib.temp_frame()
    def FWD_VALUATION(self, field, **kwds_args):
        """EXAMPLE: FWD_E2P: Forward Earning Yield = (1Yr Forward EPS Mean / Price)
        (Wtd Ave of FY1 EPS Mean & FY2 EPS Mean) / Price
        Where weights are based on fraction of year remaining in FY1 & complement
        """
        # FL:SS_E2P = SS_EPS_FWD1Y_MEAN / CLOSE
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        est_summary_lib = self.get_property(
            "est_summary_lib", field, grace=True, default_property_value="IBES2 Summary"
        )
        est_category_name = self.get_property("est_category_name", field, grace=False)
        est_stats_name = self.get_property(
            "est_stats_name", field, grace=True, default_property_value="MEAN"
        )
        dates_keyspace = RootLib()[est_summary_lib].get_property(
            "dates_keyspace", grace=False
        )

        # Get Foward Stat
        # ------------------
        fwd_stat = self.EST_FWD1Y(
            field=field,
            freq=freq,
            est_category_name=est_category_name,
            est_stats_name=est_stats_name,
            est_summary_lib=est_summary_lib,
            est_dates_keyspace=dates_keyspace,
        )

        # Get Pricing Denominator Prefix
        # Either 'CLOSE' or 'MKTCAP' (depending on est_category_name)
        if est_category_name in ("EPS", "DPS", "CFPS"):
            pricing_denom_prefix = "CLOSE"
        elif est_category_name in ("REV", "NAV"):
            pricing_denom_prefix = "MKTCAP"
        else:
            raise Exception(f"Unsupported est_category_name:{est_category_name}")

        pricing_denom = self.get_calendarized_field(
            field_prefix=pricing_denom_prefix,
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return fwd_stat / pricing_denom

    @RootLib.temp_frame()
    def VALUATION_Z5Y(self, field, **kwds_args):
        """SALES2P_Z5Y: HISTORICALLY-ADJUSTED SALES2P
        SALES2P_Z5Y = (SALES2P - MAVE(SALES2P,5*261))/MSTD(SALES2P,5*261)"""
        dates_keyspace = self.get_property("dates_keyspace", grace=False)

        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is None:
            raise Exception("Could not establish non-trivial freq property")

        periods_per_year = datetools.ppy(freq)
        if periods_per_year is None:
            raise Exception("Could not establish non-trivial periods_per_year")

        field_base = self.get_property("field_base", field, grace=False)
        base_value = self.get_calendarized_field(
            field_prefix=field_base, freq=freq, lib=self
        )

        return base_value.mz1d(
            periods=int(5 * periods_per_year),
            keyspace=dates_keyspace,
            pct_required=0.5,
            ignore_missing=True,
        )

    # =================================== PROFITABILITY / GROWTH FACTORS ==================================

    @RootLib.temp_frame()
    def ROE(self, field, **kwds_args):
        """ROE: Return on Equity (Rolling 4 Quarters)"""
        # DL:ROE_FQ = MSUM(NIB4X_FQ,4) / MMEAN(EQUITY_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        nib4extras_sum1y = self.get_fiscal_field(
            field_prefix="NI_COMMON_B4X",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        equity_mean1y = self.get_fiscal_field(
            field_prefix="EQUITY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative equity_mean1y
        equity_mean1y.conditional_nullify_inplace(equity_mean1y < 0)

        roe_fiscal = nib4extras_sum1y / equity_mean1y
        return (
            self.calendarize(roe_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else roe_fiscal
        )

    @RootLib.temp_frame()
    def ROA(self, field, **kwds_args):
        """ROA: Return on Assets (Rolling 4 Quarters)"""
        # DL:ROA_FQ = MSUM(NIB4X_FQ,4) / MMEAN(ASSETS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        nib4extras_sum1y = self.get_fiscal_field(
            field_prefix="NIB4X",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative assets_mean1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        assets_mean1y.conditional_nullify_inplace(assets_mean1y < 0)

        roa_fiscal = nib4extras_sum1y / assets_mean1y
        return (
            self.calendarize(roa_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else roa_fiscal
        )

    @RootLib.temp_frame()
    def ROAA(self, field, **kwds_args):
        """ROAA: Return on Adjusted Assets
        ROAA = Q2D(MSUM(NIB4X_FQ,4))/ADJ_ASSETS = Q2D(MSUM(NIB4X_FQ,4))/(TOTAL ASSETS + (0.1 * (EQUITY - MKTCAP)))
        Used on Distress Measures: Campbell, Hilscher & Szilagyi, 2005"""
        # FL:ROAA = Q2D(MSUM(NIB4X_FQ,4)) / ADJ_ASSETS = (Q2D(MSUM(NIB4X_FQ,4)) / (Q2D(ASSETS_FQ) + 0.1*(EQUITY-MKTCAP)))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        equity = self.get_fiscal_field(
            field_prefix="EQUITY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        mv = self.get_calendarized_field(
            field_prefix="MKTCAP",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        # Need all components to be non-missing
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        adj_assets = assets + 0.1 * (equity - mv)

        nib4x_sum1y = self.get_fiscal_field(
            field_prefix="NIB4X",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)

        # Require non-negative adjusted assets
        adj_assets.conditional_nullify_inplace(adj_assets < 0)

        roaa = nib4x_sum1y / adj_assets
        return roaa

    @RootLib.temp_frame()
    def RNOA(self, field, **kwds_args):
        """ROA: Return on Net Operating Assets (Rolling 4 Quarters)
        See "The Use of DuPont Analysis by Market Participants, Soliman (2007)"""
        # DL:RNOA_FQ = MSUM(OPINC_FQ,4) / MMEAN(NOA_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        opinc_sum1y = self.get_fiscal_field(
            field_prefix="OPINC",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        noa = self.get_fiscal_field(
            field_prefix="NOA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )

        # Require non-negative noa
        noa.conditional_nullify_inplace(noa < 0)

        rnoa = opinc_sum1y / noa
        return (
            self.calendarize(rnoa, freq=freq, add_frame=False)
            if freq is not None
            else rnoa
        )

    @RootLib.temp_frame()
    def ROIC(self, field, **kwds_args):
        """ROIC: Return on Invested Capital (Rolling 4 Quarters)
        See" 'The Productivity Premium in Equity Returns' by Brown & Row (2005)"""
        # DL:ROIC_FQ = MSUM(EBIT_FQ,4) / MMEAN(IC_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        ebit_sum1y = self.get_fiscal_field(
            field_prefix="EBIT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        ic_mean1y = self.get_fiscal_field(
            field_prefix="IC",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative ic_mean1y
        ic_mean1y.conditional_nullify_inplace(ic_mean1y < 0)

        roic_fiscal = ebit_sum1y / ic_mean1y

        return (
            self.calendarize(roic_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else roic_fiscal
        )

    @RootLib.temp_frame()
    def ROEFCF(self, field, **kwds_args):
        """ROEFCF: Free Cash Flow Return on Equity (Rolling 4 Quarters)"""
        # DL:ROEFCF_FQ = MSUM(FCF_FQ,4) / MMEAN(EQUITY_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        fcf_sum1y = self.get_fiscal_field(
            field_prefix="FCF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        equity_mean1y = self.get_fiscal_field(
            field_prefix="EQUITY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative equity_mean1y
        equity_mean1y.conditional_nullify_inplace(equity_mean1y < 0)

        roefcf = fcf_sum1y / equity_mean1y

        return (
            self.calendarize(roefcf, freq=freq, add_frame=False)
            if freq is not None
            else roefcf
        )

    @RootLib.temp_frame()
    def CFROIC(self, field, **kwds_args):
        """CFROIC: Cash Flow Return on Invested Capital (Rolling 4 Quarters)"""
        # DL:CFROIC_FQ = MSUM(CF_FQ,4) / MMEAN(IC_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        cf_sum1y = self.get_fiscal_field(
            field_prefix="CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        ic_mean1y = self.get_fiscal_field(
            field_prefix="IC",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative ic_mean1y
        ic_mean1y.conditional_nullify_inplace(ic_mean1y < 0)

        cfroic = cf_sum1y / ic_mean1y

        return (
            self.calendarize(cfroic, freq=freq, add_frame=False)
            if freq is not None
            else cfroic
        )

    @RootLib.temp_frame()
    def FCFROIC(self, field, **kwds_args):
        """FCFROIC: Free Cash Flow Return on Invested Capital (Rolling 4 Quarters)"""
        # DL:FCFROIC_FQ = MSUM(FCF_FQ,4) / MMEAN(IC_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        fcf_sum1y = self.get_fiscal_field(
            field_prefix="FCF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        ic_mean1y = self.get_fiscal_field(
            field_prefix="IC",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative ic_mean1y
        ic_mean1y.conditional_nullify_inplace(ic_mean1y < 0)

        fcfroic = fcf_sum1y / ic_mean1y

        return (
            self.calendarize(fcfroic, freq=freq, add_frame=False)
            if freq is not None
            else fcfroic
        )

    @RootLib.temp_frame()
    def CFROA(self, field, **kwds_args):
        """CFROA: Cash Flow Return on Assets (Rolling 4 Quarters)
        Used as a component in Mohanram's G-Score (Growth Score)
        see 'Separating Winners from Loosers among Low Book to Market Stocks...' by Partha Mohanram, 2004
        """
        # DL:CFROA_FQ = MSUM(CF_FQ,4) / MMEAN(ROA_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        cf_sum1y = self.get_fiscal_field(
            field_prefix="CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative assets_mean1y
        assets_mean1y.conditional_nullify_inplace(assets_mean1y < 0)

        cfroa = cf_sum1y / assets_mean1y

        return (
            self.calendarize(cfroa, freq=freq, add_frame=False)
            if freq is not None
            else cfroa
        )

    @RootLib.temp_frame()
    def PRETAXRONA(self, field, **kwds_args):
        """PRETAXRONA: Pretax Return on Net Assets (Rolling 4 Quarters)"""
        # FL:PRETAXRONA_FQ = MSUM(PRETAXINC_FQ,4) / (MMEAN(CASH_FQ,4) + MMEAN(PPE_NET_FQ,4) + MMEAN(WC_FQ,4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        pretaxinc_sum1y = self.get_fiscal_field(
            field_prefix="PRETAXINC",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        net_assets_mean1y = self.get_fiscal_field(
            field_prefix="NET_ASSETS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative net_assets_mean1y
        net_assets_mean1y.conditional_nullify_inplace(net_assets_mean1y < 0)

        pretax_rona = pretaxinc_sum1y / net_assets_mean1y

        return (
            self.calendarize(pretax_rona, freq=freq, add_frame=False)
            if freq is not None
            else pretax_rona
        )

    @RootLib.temp_frame()
    def RONA(self, field, **kwds_args):
        """RONA: Return on Net Assets (Rolling 4 Quarters)"""
        # FL:RONA_FQ = MSUM(NI_FQ,4) / (MMEAN(CASH_FQ,4) + MMEAN(PPE_NET_FQ,4) + MMEAN(WC_FQ,4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        net_income_sum1y = self.get_fiscal_field(
            field_prefix="NI",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        net_assets_mean1y = self.get_fiscal_field(
            field_prefix="NET_ASSETS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative net_assets_mean1y
        net_assets_mean1y.conditional_nullify_inplace(net_assets_mean1y < 0)

        rona = net_income_sum1y / net_assets_mean1y

        return (
            self.calendarize(rona, freq=freq, add_frame=False)
            if freq is not None
            else rona
        )

    @RootLib.temp_frame()
    def EBIT2A(self, field, **kwds_args):
        """EBIT2A: (EBIT / (Average Assets)) (Rolling 4 Quarters)"""
        # FL:EBIT2A_FQ = MSUM(EBIT_FQ,4) / MMEAN(ASSETS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        ebit_sum1y = self.get_fiscal_field(
            field_prefix="EBIT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative assets_mean1y
        assets_mean1y.conditional_nullify_inplace(assets_mean1y < 0)

        ebit2a = ebit_sum1y / assets_mean1y

        return (
            self.calendarize(ebit2a, freq=freq, add_frame=False)
            if freq is not None
            else ebit2a
        )

    @RootLib.temp_frame()
    def EBITDA2A(self, field, **kwds_args):
        """EBITDA2A: (EBITDA / (Average Assets)) (Rolling 4 Quarters)"""
        # FL:EBITDA2A_FQ = MSUM(EBITDA_FQ,4) / MMEAN(ASSETS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        ebitda_sum1y = self.get_fiscal_field(
            field_prefix="EBITDA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative assets_mean1y
        assets_mean1y.conditional_nullify_inplace(assets_mean1y < 0)

        ebitda2a = ebitda_sum1y / assets_mean1y

        return (
            self.calendarize(ebitda2a, freq=freq, add_frame=False)
            if freq is not None
            else ebitda2a
        )

    @RootLib.temp_frame()
    def CFINV2A(self, field, **kwds_args):
        """CFINV2A: (CFINV_FQ / (Average Assets)) (Rolling 4 Quarters)"""
        # FL:CFINV2A_FQ = MSUM(CFINV_FQ,4) / MMEAN(ASSETS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        cfinv_sum1y = self.get_fiscal_field(
            field_prefix="CFINV", fiscal_mode=fiscal_mode, lib=cft_lib, aggr_op1y="msum"
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
        )

        # Require non-negative assets_mean1y
        assets_mean1y.conditional_nullify_inplace(assets_mean1y < 0)

        cfinv2a = cfinv_sum1y / assets_mean1y

        return (
            self.calendarize(cfinv2a, freq=freq, add_frame=False)
            if freq is not None
            else cfinv2a
        )

    @RootLib.temp_frame()
    def SALES_GR1Y(self, field, **kwds_args):
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        sales_gr1y_fiscal = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mpctchg",
            freq=None,
        )
        return (
            self.calendarize(sales_gr1y_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else sales_gr1y_fiscal
        )

    @RootLib.temp_frame()
    def SALES_GR1Y_AVE5Y(self, field, **kwds_args):
        """SALES_GR1Y_AVE5Y_FQ: 5Y (20Q) Average of YoY (4Q) PctChange in Trailing 4Q Sales
        SALES_GR1Y_AVE5Y_FQ = MMEAN(SALES_GR1Y_FQ,20) = MMEAN(MPCTCHG(SALES_SUM4Q_FQ,4),20) = MMEAN(MPCTCHG(MSUM(SALES_FQ,4),4),20)
        Prior: High Level = Bearish (Mean reverting per Lakonsihok et.al., 1994)
        """
        # DL:SALES_GR1Y_AVE5Y_FQ = MMEAN(SALES_GR1Y_FQ,20)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        sales_gr1y_ave5y_fiscal = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mpctchg",
            multi_year_window=5,
            multi_year_op="mmean",
            freq=None,
        )
        return (
            self.calendarize(sales_gr1y_ave5y_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else sales_gr1y_ave5y_fiscal
        )

    @RootLib.temp_frame()
    def ROE_MED5Y(self, field, **kwds_args):
        """ROE_MED5Y_FQ: 5Y (20Q) Median of ROE"""
        # DL:ROE_MED5Y_FQ = MMEDIAN(ROE_FQ,20) # WHERE 20Q = 5Y
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="ROE",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            multi_year_window=5,
            multi_year_op="mmedian",
            multi_year_ignore_missing=True,
            multi_year_pct_required=0.5,
            freq=freq,
        )  # <-- Convert to calendar time/space (if applicable)

    @RootLib.temp_frame()
    def RETEARN2A(self, field, **kwds_args):
        """RETEARN2A_FQ = (Retained Earnings / Assets)"""
        # DL:RETEARN2A_FQ = (RETEARN_FQ / ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        retearn = self.get_fiscal_field(
            field_prefix="RETEARN",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        # Require non-negative assets
        assets.conditional_nullify_inplace(assets < 0)

        retearn2a_fiscal = retearn / assets

        return (
            self.calendarize(retearn2a_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else retearn2a_fiscal
        )

    @RootLib.temp_frame()
    def FWD_EPS_GR1Y(self, field, **kwds_args):
        """SS_EPS_GR1Y = [(SS_EPS_MEAN_FWD1Y / Q2D(MSUM(NI_FQ,4)/SHARES_FQ)) - 1]"""
        # FL:SS_EPS_GR1Y = [(SS_EPS_MEAN_FWD1Y / Q2D(MSUM(NI_FQ,4)/SHARES_FQ)) - 1]

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        if freq is not None:
            RootLib().set_control("freq", freq)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        ni_sum1y = self.get_fiscal_field(
            field_prefix="NI",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        shares = self.get_fiscal_field(
            field_prefix="SHARES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        eps_fy0 = ni_sum1y / shares
        if freq is not None:
            eps_fy0 = self.calendarize(eps_fy0, freq=freq, add_frame=False)

        eps_fwd1y_mean = self.EST_FWD1Y(
            field=field,
            freq=freq,
            est_category_name="EPS",
            est_stats_name="MEAN",
            est_summary_lib=est_summary_lib,
            est_dates_keyspace=dates_keyspace,
        )

        eps_fwd_gr1y = (eps_fwd1y_mean / eps_fy0) - 1.0
        return eps_fwd_gr1y

    @RootLib.temp_frame()
    def FWD_SALES_GR1Y(self, field, **kwds_args):
        """SS_SALES_GR1Y = [(SS_SALES_MEAN_FWD1Y / Q2D(MSUM(SALES_FQ,4))) - 1]"""
        # FL:SS_SALES_GR1Y = [(SS_SALES_MEAN_FWD1Y / Q2D(MSUM(SALES_FQ,4))) - 1]
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        if freq is not None:
            RootLib().set_control("freq", freq)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        sales_fy0 = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        if freq is not None:
            sales_fy0 = self.calendarize(sales_fy0, freq=freq, add_frame=False)

        sales_fwd1y_mean = self.EST_FWD1Y(
            field=field,
            freq=freq,
            est_category_name="REV",
            est_stats_name="MEAN",
            est_summary_lib=est_summary_lib,
            est_dates_keyspace=dates_keyspace,
        )

        sales_fwd_gr1y = (sales_fwd1y_mean / sales_fy0) - 1.0
        return sales_fwd_gr1y

    @RootLib.temp_frame()
    def FWD_DPS_GR1Y(self, field, **kwds_args):
        """SS_EPS_GR1Y = [(SS_EPS_MEAN_FWD1Y / Q2D(MSUM(NI_FQ,4)/SHARES_FQ)) - 1]"""
        # FL:SS_EPS_GR1Y = [(SS_EPS_MEAN_FWD1Y / Q2D(MSUM(NI_FQ,4)/SHARES_FQ)) - 1]

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        if freq is not None:
            RootLib().set_control("freq", freq)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        cash_divs_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CASHDIV_PD_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        shares = self.get_fiscal_field(
            field_prefix="SHARES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        dps_fy0 = cash_divs_sum1y / shares  # <-- Fiscal time
        if freq is not None:
            dps_fy0 = self.calendarize(dps_fy0, freq=freq, add_frame=False)

        dps_fwd1y_mean = self.EST_FWD1Y(
            field=field,
            freq=freq,
            est_category_name="DPS",
            est_stats_name="MEAN",
            est_summary_lib=est_summary_lib,
            est_dates_keyspace=dates_keyspace,
        )

        dps_fwd_gr1y = (dps_fwd1y_mean / dps_fy0) - 1.0
        return dps_fwd_gr1y

    @RootLib.temp_frame()
    def SALES_GR1Y_STD5Y(self, field, **kwds_args):
        """SALES_GR1Y_STD5Y_FQ: 5Y (20Q) Standard Deviation of YoY (4Q) PctChange in Trailing 4Q Sales
        SALES_GR1Y_STD5Y_FQ = MSTDDEV(SALES_GR1Y_FQ,20) = MSTDDEV(MPCTCHG(SALES_SUM4Q_FQ,4),20) = MSTDDEV(MPCTCHG(MSUM(SALES_FQ,4),4),20)
        Note: This measure utilized in Mohanran's G-Score (see Mohanran, 2004)
        Prior: Higher Level = Bearish (Perverse)
        """
        # DL:SALES_GR1Y_AVE5Y_FQ = MSTD(SALES_GR1Y_FQ,20)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        sales_gr1y_std5y_fiscal = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mpctchg",
            multi_year_window=5,
            multi_year_op="mstd",
            multi_year_ignore_missing=True,
            multi_year_pct_required=0.5,
            freq=None,
        )
        return (
            self.calendarize(sales_gr1y_std5y_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else sales_gr1y_std5y_fiscal
        )

    @RootLib.temp_frame()
    def MOHANRAM_G(self, field, **kwds_args):
        """MOHANRAM_G: MOHANRAN'S GROWTH SCORE = DIFFUSION INDICATOR OF EIGHT BINARY GROWTH SCORES
        MOHANRAM_G = (ROA_IND_NEUT>0)
                   + (CFROA_IND_NEUT>0)
                   + (CFOPS>NI_CF)
                   + (ROA_STD5Y_IND_NEUT<0)
                   + (SALES_GR1Y_STD5Y_IND_NEUT<0)
                   + (RND2SALES_IND_NEUT>0)
                   + (CAPEX2SALES_IND_NEUT>0)
                   + (ADV2SALES_IND_NEUT>0)
        Where: G6N represent GICS6 / Industry Neutralized (Relative) Factors
        Prior: High Level = BULLISH (High & Stable Growth Companies)
        Ideally, G-Score shold be applied in Low B/P (or High P/B) Sub-Universes
        Note: For convenience, R&D, CapEx & Advertising expense terms are normalized by sales
              (rather than by assets as per Mohanran's original paper)
        see 'Separating Winners from Loosers among Low Book to Market Stocks...' by Partha Mohanram, 2004
        """
        # FL:MOHANRAM_G = (ROA_IND_NEUT>0) + (CFROA_IND_NEUT>0) + ((CFOPS-NI_CF)>0) + (ROA_STD5Y_IND_NEUT<0) + (SALES_GR1Y_STD5Y_IND_NEUT<0) + (RND2SALES_IND_NEUT>0) + (CAPEX2SALES_IND_NEUT>0) + (ADV2SALES_IND_NEUT>0)

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        roa_ind_neut = self.get_fiscal_field(
            field_prefix="ROA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="demean",
            freq=None,
        )
        cfroa_ind_neut = self.get_fiscal_field(
            field_prefix="CFROA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="demean",
            freq=None,
        )
        cfops_sum1y = self.get_fiscal_field(
            field_prefix="CFOPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        ni_sum1y = self.get_fiscal_field(
            field_prefix="NI",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        roa_std5y_ind_neut = self.get_fiscal_field(
            field_prefix="ROA_STD5Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="demean",
            freq=None,
        )
        sales_gr1y_std5y_ind_neut = self.get_fiscal_field(
            field_prefix="SALES_GR1Y_STD5Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="demean",
            freq=None,
        )
        rnd2sales_ind_neut = self.get_fiscal_field(
            field_prefix="RND2SALES",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="demean",
            freq=None,
        )
        capex2sales_ind_neut = self.get_fiscal_field(
            field_prefix="CAPEX2SALES",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="demean",
            freq=None,
        )
        adv2sales_ind_neut = self.get_fiscal_field(
            field_prefix="ADV2SALES",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="demean",
            freq=None,
        )

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        # Note: preface each term with 1.0* expression to force dtype conversion or each term to float

        gcount = (
            roa_ind_neut.where_not_missing().change_dtype("float")
            + cfroa_ind_neut.where_not_missing().change_dtype("float")
            + (cfops_sum1y - ni_sum1y).where_not_missing().change_dtype("float")
            + roa_std5y_ind_neut.where_not_missing().change_dtype("float")
            + sales_gr1y_std5y_ind_neut.where_not_missing().change_dtype("float")
            + rnd2sales_ind_neut.where_not_missing().change_dtype("float")
            + capex2sales_ind_neut.where_not_missing().change_dtype("float")
            + adv2sales_ind_neut.where_not_missing().change_dtype("float")
        )

        gscore = (
            (roa_ind_neut > 0.0).change_dtype("float")
            + (cfroa_ind_neut > 0.0).change_dtype("float")
            + (cfops_sum1y > ni_sum1y).change_dtype("float")
            + (roa_std5y_ind_neut < 0.0).change_dtype("float")
            + (sales_gr1y_std5y_ind_neut < 0.0).change_dtype("float")
            + (rnd2sales_ind_neut > 0.0).change_dtype("float")
            + (capex2sales_ind_neut > 0.0).change_dtype("float")
            + (adv2sales_ind_neut > 0.0).change_dtype("float")
        )

        # Require non-missing content for atleast five metrics
        # Could consider using Quble.conditional_remove_inplace method
        gscore.conditional_nullify_inplace(gcount < 5)

        return (
            self.calendarize(gscore, freq=freq, add_frame=False)
            if freq is not None
            else gscore
        )

    @RootLib.temp_frame()
    def MOHANRAM_GZ(self, field, **kwds_args):
        """MOHANRAM_GZ: CONTINUOUS (Z-SCORE) VERSION OF MOHANRAN'S GROWTH SCORE = SUM OF EIGHT GROWTH Z-SCORES
        MOHANRAM_GZ = ROA_IND_Z
                    + CFROA_IND_Z
                    + IF(CFOPS>NI_CF),1,0)
                    - (ROA_STD5Y_IND_Z
                    - SALES_GR1Y_STD5Y_IND_Z
                    + RND2SALES_IND_Z
                    + CAPEX2SALES_IND_Z
                    + ADV2SALES_IND_Z
        Where: G6Z represent GICS6 / Intra-Industry Z-Score
        Prior: High Level = BULLISH (High & Stable Growth Companies)
        Ideally, G-Score shold be applied in Low B/P (or High P/B) Sub-Universes
        Note: For convenience, R&D, CapEx & Advertising expense terms are normalized by sales
              (rather than by assets as per Mohanran's original paper)
        see 'Separating Winners from Loosers among Low Book to Market Stocks...' by Partha Mohanram, 2004
        """
        # FL:MOHANRAM_GZ = ROA_IND_Z + CFROA_IND_Z + G6Z(CFOPS-NI_CF) - ROA_STD5Y_IND_Z - SALES_GR1Y_STD5Y_IND_Z + RND2SALES_IND_Z + CAPEX2SALES_IND_Z + ADV2SALES_IND_Z
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Set the environmental controls
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        # Note: preface each term with 1.0* expression to force dtype conversion or each term to float

        roa_ind_z = self.get_fiscal_field(
            field_prefix="ROA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="z",
            freq=None,
        )
        cfroa_ind_z = self.get_fiscal_field(
            field_prefix="CFROA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="z",
            freq=None,
        )
        roa_std5y_ind_z = self.get_fiscal_field(
            field_prefix="ROA_STD5Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="z",
            freq=None,
        )
        sales_gr1y_std5y_ind_z = self.get_fiscal_field(
            field_prefix="SALES_GR1Y_STD5Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="z",
            freq=None,
        )
        rnd2sales_ind_z = self.get_fiscal_field(
            field_prefix="RND2SALES",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="z",
            freq=None,
        )
        capex2sales_ind_z = self.get_fiscal_field(
            field_prefix="CAPEX2SALES",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="z",
            freq=None,
        )
        adv2sales_ind_z = self.get_fiscal_field(
            field_prefix="ADV2SALES",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            ind_norm_op="z",
            freq=None,
        )

        # Compute accruals metric...
        # --------------------------
        cfops_sum1y = self.get_fiscal_field(
            field_prefix="CFOPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        ni_sum1y = self.get_fiscal_field(
            field_prefix="NI",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        accr_cf = (
            cfops_sum1y - ni_sum1y
        )  # <-- Accruals ala Cash-Flow Statement (primary source)

        ebitda_sum1y = self.get_fiscal_field(
            field_prefix="EBITDA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        accr_inc_stmt = (
            ebitda_sum1y - ni_sum1y
        )  # <-- Accruals ala Income Statement (secondary source)

        accr = accr_cf.merge(accr_inc_stmt, self_precedence=True)

        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # While this deviates from Mohanran's original binary/diffusion formulation,
        # we need to normalize the accruals term to implement a continuous/z-score version of Mohanran's g-score
        accr2a = accr / assets_mean1y
        accr2a_ind_z = self.industry_normalization(accr2a, norm_op="z")

        # Compute gcount_z & gscore_z
        RootLib().set_control("ignore_add", False)  # <-- Intentional
        gcount_z = (
            roa_ind_z.where_not_missing().change_dtype("float")
            + cfroa_ind_z.where_not_missing().change_dtype("float")
            + accr2a_ind_z.where_not_missing().change_dtype("float")
            + roa_std5y_ind_z.where_not_missing().change_dtype("float")
            + sales_gr1y_std5y_ind_z.where_not_missing().change_dtype("float")
            + rnd2sales_ind_z.where_not_missing().change_dtype("float")
            + capex2sales_ind_z.where_not_missing().change_dtype("float")
            + adv2sales_ind_z.where_not_missing().change_dtype("float")
        )

        RootLib().set_control("ignore_add", True)
        gscore_z = (
            roa_ind_z
            + cfroa_ind_z
            + accr2a_ind_z
            - roa_std5y_ind_z
            - sales_gr1y_std5y_ind_z
            + rnd2sales_ind_z
            + capex2sales_ind_z
            + adv2sales_ind_z
        )  # <-- Note intentional use of subtraction terms here

        # Require non-missing content for atleast five metrics
        # Could consider using Quble.conditional_remove_inplace method
        gscore_z.conditional_nullify_inplace(gcount_z < 5)

        return (
            self.calendarize(gscore_z, freq=freq, add_frame=False)
            if freq is not None
            else gscore_z
        )

    # ==================================== EARNINGS QUALITY FACTORS ==========================================

    # ACCRUAL NUMERATORS ($ BASED!!)...
    # ---------------------------------
    @RootLib.temp_frame()
    def WC_ACCR_CF(self, field, **kwds_args):
        """WC_ACCR_CF: WORKING CAPITAL ACCRUALS (CASH FLOW STATEMENT FORMULATION) = SUM4Q(WORKING CAPITAL ACCRUALS) = -1 x SUM4Q(CHG_WC_CF_FQ)
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR!!!
        Using Cash Flow Formulation Here
        Where: WORKING CAPITAL ACCRUALS = Accrual Based Working Capital Changes
                                        = -1 x CHANGES IN CASH FLOW (i.e., Cash Flow Statemnet Items) Related to Changes in Working Capital
                                        = -1 x SUM4Q(WC_ACCR_CF_FQ)
                                        = -1 x SUM4Q(RECVS_CF_FQ + INV_CF_FQ + PAYABLES_CF_FQ + TAX_PAYABLE_CF_FQ + OTH_ASSETS_CF_FQ)
        Underlying Signs: 1) RECVS (Asset) Increases: Cash Flow DECREASES [aka RECVS_CF_FQ DECREASES]
                          2) INV (Asset) Increases: Cash Flow DECREASES [aka INV_CF_FQ DECREASES]
                          3) PAYABLES (Liability) Increases: Cash Flow DECREASES [aka PAYABLES_CF_FQ INCREASES]
                          4) TAX_PAYABLE (Liability) Increases: Cash Flow DECREASES [aka TAX_PAYABLE_CF_FQ INCREASES]
                          5) OTH_ASSETS (Asset) Increases: Cash Flow DECREASES [aka OTH_ASSETS_CF_FQ DECREASES]

        Note: These CF items represent changes (RECVS_CF_FQ,INV_CF_FQ,PAYABLES_CF_FQ,TAX_PAYABLE_CF_FQ,OTH_ASSETS_CF_FQ)

         ==> Prior: HIGH LEVEL = BEARISH
        See "Accrual Reversals, Earnings & Stock Returns" by Allen, Larson & Sloan (2009)
        """
        # DL:WC_ACCR_CF_FQ = MSUM(CHG_WC_CF_FQ,4)
        # DL:(PREV/INCOMPLETE FORMULA)WC_ACCR_CF_FQ = SUM4Q(RECVS_CF_FQ + INV_CF_FQ + PAYABLES_CF_FQ + TAX_PAYABLE_FQ + OTH_ASSETS_CF_FQ)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # BECAUSE USES of cash (aka a change in WC) reflect a negative cash flow number,
        # WE MUST FLIP SIGN TO GET ACTUAL CHANGE IN WC
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        chg_wc_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CHG_WC_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        return (
            self.calendarize(chg_wc_sum1y, freq=freq, add_frame=False)
            if freq is not None
            else chg_wc_sum1y
        )

    @RootLib.temp_frame()
    def OP_ACCR_CF(self, field, **kwds_args):
        """OP_ACCR_CF: OPERATING ACCRUALS (C/F METHOD)
        Where: OPERATING ACCRUALS (C/F) = (MSUM(NI_CF_FQ,4) - MSUM(CFOPS_FQ,4))
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR!!!
        Using Cash Flow Formulation Here
        """
        # DL:OP_ACCR_CF_FQ = (MSUM(NI_CF_FQ,4) - MSUM(CFOPS_FQ,4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        ni_cf_sum1y = self.get_fiscal_field(
            field_prefix="NI_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        cfops_sum1y = self.get_fiscal_field(
            field_prefix="CFOPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        result = ni_cf_sum1y - cfops_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def WC(self, field, **kwds_args):
        """Working Capital
        WC = RECEIVABLES + INVENTORY + PAYABLES
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR!!!"""
        # DL:WC_FQ = (RECEIVABLES_FQ + INVENTORY_FQ - PAYABLES_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        recv = self.get_fiscal_field(
            field_prefix="RECEIVABLES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        inv = self.get_fiscal_field(
            field_prefix="INVENTORY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        payables = self.get_fiscal_field(
            field_prefix="PAYABLES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        # Note: No inventory may be recorded as missing inventory value
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        wc = recv + inv + payables
        return (
            self.calendarize(wc, freq=freq, add_frame=False) if freq is not None else wc
        )

    @RootLib.temp_frame()
    def OP_ACCR_BS(self, field, **kwds_args):
        """OP_ACCR_BS: OPERATING ACCRUALS (B/S METHOD)
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR!!!
        Where: OPERATING ACCRUALS (B/S) = YoY Change(WC - CASH - ACCUM_DEPR)
        Using Balance Sheet Approach, Per Beneish (1999) [NOTE: Beneish call this 'Total Accruals']
        """
        # DL:OP_ACCR_BS_FQ = MDIFF4Q(WC_FQ - CASH_FQ - ACCUM_DEPR_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        wc = self.get_fiscal_field(
            field_prefix="WC",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        accum_depr = self.get_fiscal_field(
            field_prefix="ACCUM_DEPR",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- WORKING CAPITAL BELOW IS REQUIRED TO BE NON-MISSING
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        op_accruals_bs = wc - cash - accum_depr
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        op_accruals_bs_diff1y = op_accruals_bs.mdiff1d(
            fiscal_ppy, keyspace=fiscal_keyspace
        )
        return (
            self.calendarize(op_accruals_bs_diff1y, freq=freq, add_frame=False)
            if freq is not None
            else op_accruals_bs_diff1y
        )

    @RootLib.temp_frame()
    def TOT_ACCR_CF(self, field, **kwds_args):
        """TOT_ACCR_CF_FQ: TOTAL ACCRUALS (C/F METHOD)
        Where: TOTAL ACCRUALS (CASH FLOW APPROACH) = (MSUM(NI_CF_FQ,4)
                                                     -MSUM(CFOPS_FQ,4)
                                                     -MSUM(CFINV_FQ,4)
                                                     -MSUM(CFFIN_FQ,4)
                                                     +MSUM(NET_STK_ISSUANCE_CF_FQ,4)
                                                     -MSUM(-1.*CASHDIV_PD_CF_FQ,4))   NOTE: (CASHDIV_PD_CF_FQ < 0)
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR!!!
        Using Cash Flow Formulation Here, See Richardson et.al.(2005), Dechow (2006) or Hafzalla et.al (2010)
        """
        # DL:TOT_ACCR_CF_FQ = (MSUM(NI_CF_FQ,4)-MSUM(CFOPS_FQ,4)-MSUM(CFINV_FQ,4)-MSUM(CFFIN_FQ,4)+MSUM(NET_STK_ISSUANCE_CF_FQ,4)-MSUM(1.*CASHDIV_PD_CF_FQ,4))  NOTE: (CASHDIV_PD_CF_FQ < 0)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        ni_cf_sum1y = self.get_fiscal_field(
            field_prefix="NI_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        cfops_sum1y = self.get_fiscal_field(
            field_prefix="CFOPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # CONVENTION: CFINV_FQ  < 0 (CASH SPENT)
        cfinv_sum1y = self.get_fiscal_field(
            field_prefix="CFINV",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # CONVENTION: CFFIN_FQ < 0 (CASH SPENT)
        cffin_sum1y = self.get_fiscal_field(
            field_prefix="CFFIN",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # CONVENTION: NET_STK_ISSUANCE_CF > 0 (CASH RECEIVED)
        cf_net_stk_issue_sum1y = self.get_fiscal_field(
            field_prefix="NET_STK_ISSUANCE_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # CONVENTION: CASHDIV_PD_CF < 0 (CASH SPENT)
        # ----------------------------------------------------------------------------------------------------------------------------
        # Note: Reuters-Fundamental CASHDIV_PD_CF_FQ (RF Item: FCDP) is quoted < 0 (logic: uses cash flow therefore negative).
        # However, the analogous Compustat (Annual Item:127) often (referenced in academic papers) is suspected to to be quoted > 0
        # ----------------------------------------------------------------------------------------------------------------------------
        cf_div_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CASHDIV_PD_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # ----------------------------------------------------------------------------------------------------------------------------
        # Note: Net stock issuance (aka cf_net_stk_issue>0) will raise cash & contrib positively to cffin which is subtracted here (net negative to expression), so add cf_net_stk_issue back
        # Note: Payment of (positively quoted) cash dividends (aka cf_div=(-1*CASHDIV_PD_CF_FQ)>0) will lower cash & contrib negatively to cffin which is subtracted here (net positive to expression), so subtract (cf_div>0) amount back
        # ----------------------------------------------------------------------------------------------------------------------------

        # Full formula is as follows, but we perform in steps to control for ignore_add at each step accordingly
        # result = (ni_cf_sum1y - cfops_sum1y - cfinv_sum1y - cffin_sum1y + cf_net_stk_issue_sum1y - cf_div_sum1y)

        RootLib().set_control(
            "ignore_add", True
        )  # <-- OK FOR cfops_sum1y OR cfinv_sum1y OR cffin_sum1y TO BE MISSING
        net_cash_flow = cfops_sum1y + cfinv_sum1y + cffin_sum1y

        RootLib().set_control(
            "ignore_add", False
        )  # NEED BOTH ni_cf_sum1y & net_cash_flow TO BE NON-MISSING
        partial_accr = ni_cf_sum1y - net_cash_flow

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- partial_accr BELOW IS REQUIRED TO BE NON-MISSING, OTHERS CAN ME MISSING
        # Stock issuance will contrib positively to cffin > 0
        # Recall that cf_div_sum1y > 0 due to sign adjustment earlier
        tot_accr = partial_accr + cf_net_stk_issue_sum1y - cf_div_sum1y

        return (
            self.calendarize(tot_accr, freq=freq, add_frame=False)
            if freq is not None
            else tot_accr
        )

    # (NORMALIZED) ACCRUAL FACTORS...
    # ---------------------------------

    @RootLib.temp_frame()
    def WC_ACCR_CF2A(self, field, **kwds_args):
        """WC_ACCR_CF2A_FQ: SUM4Q(WORKING CAPITAL ACCRUALS) / AVE TOTAL ASSETS
        Using Cash Flow Formulation Here
        Where: WORKING CAPITAL ACCRUALS = Accrual Based Working Capital Changes
                                        = -1 x CHANGES IN CASH FLOW (i.e., Cash Flow Statemnet Items) Related to Changes in Working Capital
                                        = -1 x SUM4Q(WC_ACCR_CF_FQ)
                                        = -1 x SUM4Q(RECVS_CF_FQ + INV_CF_FQ + PAYABLES_CF_FQ + TAX_PAYABLE_CF_FQ + OTH_ASSETS_CF_FQ)
        Underlying Signs: 1) RECVS (Asset) Increases: Cash Flow DECREASES [aka RECVS_CF_FQ DECREASES]
                          2) INV (Asset) Increases: Cash Flow DECREASES [aka INV_CF_FQ DECREASES]
                          3) PAYABLES (Liability) Increases: Cash Flow DECREASES [aka PAYABLES_CF_FQ INCREASES]
                          4) TAX_PAYABLE (Liability) Increases: Cash Flow DECREASES [aka TAX_PAYABLE_CF_FQ INCREASES]
                          5) OTH_ASSETS (Asset) Increases: Cash Flow DECREASES [aka OTH_ASSETS_CF_FQ DECREASES]

          ==> Prior: HIGH LEVEL = BEARISH
        See "Accrual Reversals, Earnings & Stock Returns" by Allen, Larson & Sloan (2009)
        """
        # DL:WC_ACCR_CF2A_FQ = WC_ACCR_CF/ASSETS_AVE4Q_FQ = SUM4Q(CHG_WC_CF_FQ)/ASSETS_AVE4Q_FQ
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # CONVENTION: USES of cash (aka a change in WC) as a negative cash flow number,
        #         ==> WE MUST FLIP SIGN TO GET ACTUAL CHANGE IN WC
        wc_accr_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CHG_WC_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        wca2a = wc_accr_sum1y / assets_mean1y
        return (
            self.calendarize(wca2a, freq=freq, add_frame=False)
            if freq is not None
            else wca2a
        )

    @RootLib.temp_frame()
    def OP_ACCR_CF2NI(self, field, **kwds_args):
        """OP_ACCR_CF2NI_FQ = (OP_ACCR2NI_CF_FQ / ABS(NI_CF_FQ)) = ((NI_CF_FQ - CFOPS_FQ) / ABS(NI_CF_FQ))
        Where: OPERATING ACCRUALS (CASH FLOW APPROACH) = (NI_CF_FQ - CFOPS_FQ_SUM4Q)
        aka 'Percent Accruals' (see Hafzalla, Lundholm & Van Winkle, 2010)
        Statement of Cash Flow Approach
        Prior: HIGH LEVEL = BEARISH (Accruals are Dangerous)
        """
        # DL:OP_ACCR_CF2NI_FQ = (OP_ACCR_CF_FQ / ABS(MSUM(NI_CF_FQ,4))) = ((MSUM(NI_CF_FQ,4) - MSUM(CFOPS_FQ,4)) / ABS(MSUM(NI_CF_FQ,4)))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        op_accr_cf_sum1y = self.get_fiscal_field(
            field_prefix="OP_ACCR_CF",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="msum",
            freq=None,
        )
        ni_cf_sum1y = self.get_fiscal_field(
            field_prefix="NI_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        result = op_accr_cf_sum1y / ni_cf_sum1y.absolute()
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def OP_ACCR_CF2A(self, field, **kwds_args):
        """OP_ACCR2A_CF: OPERATING ACCRUALS / AVE TOTAL ASSETS
        Where: OPERATING ACCRUALS (CASH FLOW APPROACH) = (NI_CF_FQ - CFOPS_FQ_SUM4Q)
        Statement of Cash Flow Approach (See Sloan (1996))
        Prior: HIGH LEVEL = BEARISH (Higher Accruals are Dangerous)
        """
        # DL:OP_ACCR_CF2A_FQ = OP_ACCR_CF_FQ / AVE4Q(ASSETS_FQ) = (NIB4X_SUM4Q - CFOPS_FQ_SUM4Q) / AVE4Q(ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        RootLib().set_control("ignore_mult", False)

        op_accr_cf_sum1y = self.get_fiscal_field(
            field_prefix="OP_ACCR_CF",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="msum",
            freq=None,
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        op_accr_cf2a = op_accr_cf_sum1y / assets_mean1y
        return (
            self.calendarize(op_accr_cf2a, freq=freq, add_frame=False)
            if freq is not None
            else op_accr_cf2a
        )

    @RootLib.temp_frame()
    def OP_ACCR_BS2A(self, field, **kwds_args):
        """OP_ACCR_BS2A_FQ: OPERATING ACCRUALS (B/S METHOD) / AVE TOTAL ASSETS
        Where: OPERATING ACCRUALS = YoY Change(WC - CASH - DEPR)
        Balance Sheet Approach, Per Beneish (1999) [NOTE: Beneish calls this 'total accruals' - very confusing!]
        Prior: HIGH LEVEL = BEARISH (Accruals are Dangerous)
        """
        # DL:OP_ACCR_BS2A_FQ = OP_ACCR_BS/AVE4Q(ASSETS_FQ) = MDIFF4Q(WC_FQ - CASH_FQ - ACCUM_DEPR_FQ)/AVE4Q(ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        op_accr_bs_sum1y = self.get_fiscal_field(
            field_prefix="OP_ACCR_BS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="msum",
            freq=None,
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        op_accr_bs2a = op_accr_bs_sum1y / assets_mean1y
        return (
            self.calendarize(op_accr_bs2a, freq=freq, add_frame=False)
            if freq is not None
            else op_accr_bs2a
        )

    @RootLib.temp_frame()
    def TOT_ACCR_CF2A(self, field, **kwds_args):
        """TOT_ACCR2A_CF: TOTAL ACCRUALS / AVE TOTAL ASSETS
        Where: TOTAL ACCRUALS (CASH FLOW APPROACH) = (MSUM(NI_CF_FQ,4)
                                                     -MSUM(CFOPS_FQ,4)
                                                     -MSUM(CFINV_FQ,4)
                                                     -MSUM(CFFIN_FQ,4)
                                                     +MSUM(NET_STK_ISSUANCE_CF_FQ,4)
                                                     -MSUM(-1.*CASHDIV_PD_CF_FQ,4))   NOTE: (CASHDIV_PD_CF_FQ < 0)
        Using Cash Flow Formulation Here, See Richardson et.al.(2005) or Hafzalla et.al (2010)
        Prior: HIGH LEVEL = BEARISH (Higher Accruals are Dangerous)
        """
        # DL:TOT_ACCR_CF2A_FQ = TOT_ACCR_CF_FQ / AVE4Q(ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        tot_accr_cf_sum1y = self.get_fiscal_field(
            field_prefix="TOT_ACCR_CF",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="msum",
            freq=None,
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        tot_accr_cf2a = tot_accr_cf_sum1y / assets_mean1y
        return (
            self.calendarize(tot_accr_cf2a, freq=freq, add_frame=False)
            if freq is not None
            else tot_accr_cf2a
        )

    @RootLib.temp_frame()
    def ROA_PCHG1Y(self, field, **kwds_args):
        """ROA_PCHG4Q_FQ = PCTCHG4Q(ROA)
        ROA_PCHG4Q_FQ is a factor in Piotroski's F-Score
        See also:"""
        # DL:ROA_PCHG1Y_FQ = MPCTCHG(ROA_FQ,4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="ROA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def ROA_DIFF1Y(self, field, **kwds_args):
        """ROA_DIFF4Q_FQ = DIFF4Q(ROA)
        ROA_PCHG4Q_FQ is a factor in Piotroski's F-Score
        See also:"""
        # DL:ROA_DIFF1Y_FQ = MDIFF(ROA_FQ,4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="ROA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=freq,
        )

    @RootLib.temp_frame()
    def LTD2A_PCHG1Y(self, field, **kwds_args):
        """LTD2A_PCHG1Y = PCTCHG4Q(Long Term Debt / Assets)
        LTD2A_PCHG1Y is a factor in Piotroski's F-Score
        Prior: HIGH LEVEL = BEARISH (Debt Load Increases can be Problematic)
        """
        # DL:LTD2A_PCHG1Y_FQ = MPCTCHG((LTD_FQ/ASSETS_FQ),4) = MPCTCHG4Q(LTD2A_FQ,4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="LTD2A",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def LTD2A_DIFF1Y(self, field, **kwds_args):
        """LTD2A_DIFF1Y = DIFF4Q(Long Term Debt / Assets)
        LTD2A_DIFF1Y is a factor in Piotroski's F-Score"""
        # DL:LTD2A_DIFF1Y = MDIFF(LTD_FQ/ASSETS_FQ),4) = MDIFF(LTD2A_FQ,4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="LTD2A",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=freq,
        )

    @RootLib.temp_frame()
    def CURR_RATIO_PCHG1Y(self, field, **kwds_args):
        """Current Ratio = YoY PctChg (Current Assets / Current Liabilities)
        CURR_RATIO_PCHG1Y is a factor in Piotroski's F-Score"""
        # FL:CURR_RATIO_PCH1Y = MPCTCHG(CURR_RATIO_FQ,4) = MPCTCHG((CURR_ASSETS_FQ / CURR_LIAB_FQ),4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="CURR_RATIO",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def CURR_RATIO_DIFF1Y(self, field, **kwds_args):
        """Current Ratio = YoY DIFFERNCE (Current Assets / Current Liabilities)
        CURR_RATIO_DIFF1Y is a factor in Piotroski's F-Score"""
        # FL:CURR_RATIO_DIFF4Q_FQ = MDIFF(CURR_RATIO_FQ,4) = MDIFF((CURR_ASSETS_FQ / CURR_LIAB_FQ),4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="CURR_RATIO",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=freq,
        )

    @RootLib.temp_frame()
    def ASSET_TURNOVER_PCHG1Y(self, field, **kwds_args):
        """ASSET_TURNOVER_PCHG1Y: PCTCHG4Q(SALES_SUM4Q / ASSET_AVE4Q) (Rolling 4 Quarters)
        ASSET_TURNOVER_PCHG1Y is a factor in Piotroski's F-Score"""
        # DL:ASSET_TURNOVER_PCHG4Q_FQ = MPCTCHG(ASSET_TURNOVER_FQ,4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="ASSET_TURNOVER",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def ASSET_TURNOVER_DIFF1Y(self, field, **kwds_args):
        """ASSET_TURNOVER_DIFF1Y: DIFF4Q(SALES_SUM4Q / ASSET_AVE4Q) (Rolling 4 Quarters)
        ASSET_TURNOVER_DIFF1Y is a factor in Piotroski's F-Score"""
        # DL:ASSET_TURNOVER_DIFF1Y = MPCTCHG(ASSET_TURNOVER_FQ,4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="ASSET_TURNOVER",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=freq,
        )

    # (OTHER) EARNINGS MANIPULATION FACTORS (ala BENEISH, 1999)...
    # ---------------------------------------------------------------
    @RootLib.temp_frame()
    def TAX_RATE_DIFF1Y(self, field, **kwds_args):
        """TAX_RATE_DIFF1Y: 4Q DIFFERENTIAL CHANGE IN (EFFECTIVE) TAX RATE
        TAX_RATE_DIFF1Y = MDIFF(TAX_RATE_FQ,4)
        Prior: HIGH LEVEL = BULLISH; LOW LEVEL = BEARISH
        ==> Big Reduction in Tax Rate is Interpreted as Earnings Manipulation"""
        # DL:TAX_RATE_DIFF4Q_FQ = MDIFF(TAX_RATE_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="TAX_RATE",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mdiff",
            freq=freq,
        )

    @RootLib.temp_frame()
    def DSO_PCHG1Y(self, field, **kwds_args):
        """DSO_PCHG4Q_FQ: YoY Change in DSO (ala Beneish, 1999)
        DSO_PCHG4Q_FQ = ((DSO_FQ(Q)/DSO_FQ(Q-4))-1)
        Higher Level (DSOs Increasing) = BEARISH
        """
        # DL:DSO_PCHG4Q_FQ = ((DSO_FQ(Q)/DSO_FQ(Q-4))-1)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="DSO",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def DAYS_PAY_PCHG1Y(self, field, **kwds_args):
        """DAYS_PAY_PCHG1Y: YoY Change in DSO (ala Beneish, 1999)
        DAYS_PAY_PCHG1Y = ((DAYS_PAY_FQ(Q)/DAYS_PAY_FQ(Q-4))-1)
        Financial Theory: Higher Level (Days Payable Increasing) = BULLISH (Efficient use of Working Capital)
        Empirical: Higher Level (Days Payable Increasing) = BEARISH...Intrepretation, indicates firm is having trouble paying.
        """
        # DL:DAYS_PAY_PCHG4Q_FQ = ((DAYS_PAY_FQ(Q)/DAYS_PAY_FQ(Q-4))-1)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="DAYS_PAY",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def MARGIN_GP_PCHG1Y(self, field, **kwds_args):
        """MARGIN_GP_PCHG1Y: YoY PctChg Gross Margin (ala Beneish, 1999):
        MARGIN_GP_PCHG1Y = ((MARGIN_GP_FQ(Q)/MARGIN_GP_FQ(Q-4)) - 1)
        Higher Level (Gross Margins Improving) = BULLISH
        -------------------------------------------------------
        MARGIN_GP_PCHG1Y is a factor in Piotroski's F-Score & Beneish's M-Score
        Note: Beneish uses (1/(MARGIN_GP_PCHG1Y+1)) in manipulation model (has opposite directionality)
        See "Fundamental Information Analysis" by Lev & Thiagarajan (1993)
        or "Abnormal Returns to Fundamental Analysis Strategy" by Abarbanell & Bushee (1997)
        or "The Detection of Earnings Manipulation" by Beneish (1999)"""
        # DL:MARGIN_GP_PCHG1Y = ((MARGIN_GP_FQ(Q)/MARGIN_GP_FQ(Q-4))-1)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="MARGIN_GP",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def MARGIN_GP_DIFF1Y(self, field, **kwds_args):
        """MARGIN_GP_DIFF1Y: YoY DIFFERENCE in Gross Margin (ala Beneish, 1999):
        MARGIN_GP_DIFF1Y = (MARGIN_GP_FQ(Q) - MARGIN_GP_FQ(Q-4))
        Higher Level (Gross Margins Improving) = BULLISH
        -------------------------------------------------------
        MARGIN_GP_DIFF1Y is a factor in Piotroski's F-Score & Beneish's M-Score
        Note: Beneish uses (1/(MARGIN_GP_PCHG4Q_FQ+1)) in manipulation model (has opposite directionality)
        See "Fundamental Information Analysis" by Lev & Thiagarajan (1993)
        or "Abnormal Returns to Fundamental Analysis Strategy" by Abarbanell & Bushee (1997)
        or "The Detection of Earnings Manipulation" by Beneish (1999)"""
        # DL:MARGIN_GP_PCHG4Q_FQ = ((MARGIN_GP_FQ(Q)/MARGIN_GP_FQ(Q-4))-1)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="MARGIN_GP",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=freq,
        )

    @RootLib.temp_frame()
    def ASSET_LOW_QUALITY_PCHG1Y(self, field, **kwds_args):
        """ASSET_LOW_QUALITY_PCHG1Y: YoY PctChange in Low Asset Quality (ala Beneish, 1999)
        ASSET_LOW_QUALITY_PCHG1Y = ((ASSET_LOW_QUALITY_FQ(Q)/ASSET_LOW_QUALITY_FQ(Q-4))-1)
        Where: ASSET_LOW_QUALITY = ((ASSETS - CURR_ASSETS - PPE_GROSS) / ASSETS)
        Prior: HIGH LEVEL (Low Asset Quality Increasing) = BEARISH
        Beneish(1999): "indicates that the firm has potentially increased involvement in cost deferral" (bad)
        """
        # DL:ASSET_LOW_QUALITY_PCHG1Y = ((ASSET_LOW_QUALITY_FQ(Q)/ASSET_LOW_QUALITY_FQ(Q-4)) - 1)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="ASSET_LOW_QUALITY",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def DEPR_RATE(self, field, **kwds_args):
        """DEPR_RATE_FQ: Depreciation Rate (ala Beneish, 1999)
        DEPR_RATE_FQ = DEPR_SUM4Q_FQ/(DEPR_SUM4Q_FQ + PPE_NET_FQ)
        Higher Level (Depreciation Rate Increasing) = BEARISH(?)
        Beneish (1999): Growth firms "are more likely to commit financial statement fraud" (bad)
        """
        # DL:DEPR_RATE_FQ = DEPR_SUM4Q_FQ/(DEPR_SUM4Q_FQ + PPE_NET_FQ)

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        depr_sum1y = self.get_fiscal_field(
            field_prefix="DEPR",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        ppe_net = self.get_fiscal_field(
            field_prefix="PPE_NET",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        depr_rate = depr_sum1y / (depr_sum1y + ppe_net)  # <-- In fiscal time/space
        return (
            self.calendarize(depr_rate, freq=freq, add_frame=False)
            if freq is not None
            else depr_rate
        )

    @RootLib.temp_frame()
    def DEPR_RATE_PCHG1Y(
        self, field, **kwds_args
    ):  # USE...ACCUM_DEPR(B/S) or DEPR (I/S)???
        """DEPR_RATE_PCHG1Y: YoY PctChg in Depreciation Rate (ala Beneish, 1999)
        DEPR_RATE_PCHG1Y = (DEPR_RATE_FQ(Q-4)/DEPR_RATE_FQ(Q)-1)
        Where: DEPR_RATE_FQ = DEPR_SUM4Q_FQ/(DEPR_SUM4Q_FQ + PPE_NET_FQ)
        Prior: HIGH LEVEL (Depreciation Rate Increasing) = BULLISH (Artificial/Temporary Loss of Profitability)
        Prior: LOW LEVEL (Depreciation Rate Decresing) = BEARISH (Artificial/Temporary Boost to Profitability)
        Note: Beneish uses (1/(DEPR_RATE_PCHG1Y+1)) in manipulation model (has opposite directionality)
        """
        # DL:DEPR_RATE_PCHG1Y = ((DEPR_RATE_FQ(Q-4)/DEPR_RATE_FQ(Q))-1)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="DEPR_RATE",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def MARGIN_SGA_PCHG1Y(self, field, **kwds_args):
        """MARGIN_SGA_PCHG1Y: YOY Pct Chg in SG&A Margin (ala Beneish, 1999)
        Prior: HIGH LEVEL (SGA Expense Ratio Increasing) = BEARISH
        """
        # DL:MARGIN_SGA_PCHG1Y = ([MARGIN_SGA_FQ]/[MARGIN_SGA_FQ(Q-4)] - 1)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="MARGIN_SGA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def MARGIN_SGA_DIFF1Y(self, field, **kwds_args):
        """MARGIN_SGA_DIFF1Y: YOY DIFFERENCE in SG&A Margin (ala Beneish, 1999)
        Prior: HIGH LEVEL (SGA Expense Ratio Increasing) = BEARISH
        """
        # DL:MARGIN_SGA_PCHG4Q_FQ = [MARGIN_SGA_FQ] - [MARGIN_SGA_FQ(Q-4)]
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="MARGIN_SGA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=freq,
        )

    @RootLib.temp_frame()
    def L2A_PCHG1Y(self, field, **kwds_args):
        """L2A_PCHG1Y: YoY Chg in (Liabilities/Assets) (ala Beneish, 1999)
        L2A_PCHG1Y =  ((L2A(Q)/L2A(Q-4))-1)
        Where: L2A = [LIAB/ASSETS]
        Higher Level (Liab/Assets Increasing) = BEARISH
        """
        # DL:L2A_PCHG1Y = [LIAB(Q)/ASSETS(Q)]/[LIAB(Q-4)/ASSETS(Q-4)] - 1
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="L2A",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def L2A_DIFF1Y(self, field, **kwds_args):
        """L2A_DIFF1Y: YoY DIFFERENCE in (Liabilities/Assets) (ala Beneish, 1999)
        L2A_DIFF1Y =  (L2A(Q) - L2A(Q-4))
        Where: L2A = [LIAB/ASSETS]
        Higher Level (Liab/Assets Increasing) = BEARISH
        """
        # DL:L2A_DIFF1Y = [LIAB(Q)/ASSETS(Q)] - [LIAB(Q-4)/ASSETS(Q-4)]
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="L2A",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=freq,
        )

    @RootLib.temp_frame()
    def BENEISH_MSCORE(self, field, **kwds_args):
        """BENEISH_MSCORE = EARNINGS MANIPULATION SCORE
        "The Detection of Earnings Manipulation" by Beneish (1999)

        BENEISH_MSCORE = -4.84
                     + 0.920 * (DSO_IDX_FQ)
                     + 0.528 * (GM_RIDX_FQ)
                     + 0.404 * (ASSET_LOW_QUALITY_IDX_FQ)
                     + 0.892 * (SALES_GR_IDX_FQ)
                     + 0.115 * (DEPR_RIDX_FQ)
                     - 0.172 * (SGA_EXP_IDX_FQ)
                     + 4.679 * (OP_ACCR2A_BS_FQ)
                     - 0.327 * (L2A_IDX_FQ)

        BENEISH_MSCORE = -4.84
                     + 0.920 * (DSO_PCHG4Q_FQ + 1)
                     + 0.528 * (1 / (MARGIN_GP_PCHG4Q_FQ + 1))
                     + 0.404 * (ASSET_LOW_QUALITY_PCHG4Q_FQ + 1)
                     + 0.892 * (SALES_GR1Y_FQ + 1)
                     + 0.115 * (1 / (DEPR_RATE_PCHG4Q_FQ + 1))
                     - 0.172 * (MARGIN_SGA_PCHG4Q_FQ + 1)
                     + 4.679 * (OP_ACCR_BS2A_FQ)
                     - 0.327 * (L2A_PCHG4Q_FQ + 1)

         WHERE: ASSET_LOW_QUALITY = ((NON_CURR_ASSETS-PPE_GROSS)/ASSETS) = ((ASSETS-CURR_ASSETS-PPE_GROSS)/ASSETS)
         Prior: HIGH LEVEL = BEARISH (High Manipulation Score)
        """
        # DL:BENEISH_MSCORE = (-4.84 + 9.2*DSO_IDX_FQ + 0.528*GM_RIDX_FQ \
        #                + 0.404*ASSET_LOW_QUALITY_IDX_FQ + 0.892*SALES_GR_IDX_FQ \
        #                + 0.115*DEPR_RIDX_FQ -0.172*SGA_EXP_IDX_FQ \
        #                + 4.679*OP_ACCR2A_BS_FQ - 0.327*L2A_IDX_FQ)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Access required components (in fiscal time/space)
        # ---------------------------------------------------
        dso_pctchg1y = self.get_fiscal_field(
            field_prefix="DSO_PCHG1Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        gm_pctchg1y = self.get_fiscal_field(
            field_prefix="MARGIN_GP_PCHG1Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        aq_pctchg1y = self.get_fiscal_field(
            field_prefix="ASSET_LOW_QUALITY_PCHG1Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        sales_gr1y = self.get_fiscal_field(
            field_prefix="SALES_GR1Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        depr_rate_pctchg1y = self.get_fiscal_field(
            field_prefix="DEPR_RATE_PCHG1Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        sga_margin_pctchg1y = self.get_fiscal_field(
            field_prefix="MARGIN_SGA_PCHG1Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        l2a_pctchg1y = self.get_fiscal_field(
            field_prefix="L2A_PCHG1Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )

        dso_idx = dso_pctchg1y + 1.0
        gm_ridx = 1.0 / (gm_pctchg1y + 1.0)
        aq_idx = aq_pctchg1y + 1.0
        sales_gr_idx = sales_gr1y + 1.0
        depr_ridx = 1.0 / (depr_rate_pctchg1y + 1.0)
        sga_exp_idx = sga_margin_pctchg1y + 1.0
        # Beneish actually uses Operating Accruals but refers to it as 'Total Accruals'(!)
        tata = self.get_fiscal_field(
            field_prefix="OP_ACCR_BS2A",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        l2a_idx = l2a_pctchg1y + 1.0

        beneish_mscore = (
            -4.84
            + 0.920 * (dso_idx)
            + 0.528 * (gm_ridx)
            + 0.404 * (aq_idx)
            + 0.892 * (sales_gr_idx)
            + 0.115 * (depr_ridx)
            - 0.172 * (sga_exp_idx)
            + 4.679 * (tata)
            - 0.327 * (l2a_idx)
        )

        return (
            self.calendarize(beneish_mscore, freq=freq, add_frame=False)
            if freq is not None
            else beneish_mscore
        )

    @RootLib.temp_frame()
    def MARGIN_SPECIALS(self, field, **kwds_args):
        """MARGIN_SPECIALS = MSUM(SPECIAL_ITEMS_FQ,4) / MSUM(SALES_FQ,4)
        SPECIAL ITEMS (RF:STSI): Restructuing Charges, Gain/Loss on Sale of Assets,
                                 Litigation Charges, Purchased R&D Write-Offs....
        HIGH LEVEL = BEARISH (Mean reverting...Investors overreact to special items)
        See: "Do Stock Prices Fully Reflect the Implications of Special Items for Future Earnings?" by Burgstahler et.al.(2002)
        Also: "Mispricing of Special Items & Accruals: One Anomoly or Two" by Atwood (2005)
        """
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # NOTE: SPECIAL_ITEMS MAY BE EXPLICITLY AVIALABLE WITH CERTAIN FUNDAMANTAL PROVIDERS
        specials_sum1y = self.get_fiscal_field(
            field_prefix="SPECIAL_ITEMS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # Make sure sales records are non-negative
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0.0)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        margin_specials = specials_sum1y / sales_sum1y
        return (
            self.calendarize(margin_specials, freq=freq, add_frame=False)
            if freq is not None
            else margin_specials
        )

    @RootLib.temp_frame()
    def MARGIN_SPECIALS_LAG1Y(self, field, **kwds_args):
        """MARGIN_SPECIALS_LAG4Q_FQ = MLAG(MARGIN_SPECIALS_FQ,4)
        SPECIAL ITEMS (RF:STSI): Restructuing Charges, Gain/Loss on Sale of Assets,
                                 Litigation Charges, Purchased R&D Write-Offs....
        HIGH LEVEL = BULLISH (Atwood, 2005: In First Year: Investors overreact to specials; Afterward 1st year: Specials help)
        See: "Do Stock Prices Fully Reflect the Implications of Special Items for Future Earnings?" by Burgstahler et.al.(2002)
        Also: "Mispricing of Special Items & Accruals: One Anomoly or Two" by Atwood (2005)
        """
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="MARGIN_SPECIALS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="shift",
            freq=freq,
        )

    # "UNEXPECTED" FACTORS...
    # --------------------------
    @RootLib.temp_frame()
    def UNEXP_GP(self, field, **kwds_args):
        """UNEXP_GP_FQ: UNEXPECTED GROSS PROFIT
        See 'Fundamental Information Analysis' by Lev & Thiagarajan (1993)
        or 'Abnormal Returns to Fundamental Analysis Strategy' by Abarbanell & Bushee (1997)
        A&B: 'GM indicates an improvement (deterioration) in the firm's trade and hence, expected operating performance'
        """
        # DL:UNEXP_GP_FQ = [GP_FQ - (MLAG(GP_FQ,4) * (MSUM(SALES_FQ,4) / MLAG(MSUM(SALES_FQ,4),4)))] / MLAG(ASSETS_FQ,4)

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        return self.get_fiscal_unexp(
            src_field_prefix="GP",
            scale_field_prefix="SALES",
            denom_field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            src_aggr_op1y="msum",
            scale_aggr_op1y="msum",
            denom_aggr_op1y=None,
            fiscal_keyspace=fiscal_keyspace,
            freq=freq,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def UNEXP_AP(self, field, **kwds_args):
        """UNEXP_AP: UNEXPECTED PAYABLES
        Prior: HIGH LEVEL = BEARISH
        ==> Growth in Accounts Payables represents a delay in payments which may reflect a cash flow shortage
        Prior: HIGH LEVEL = BEARISH"""
        # DL:UNEXP_AP_FQ = [PAYABLES_FQ - (MLAG(PAYABLES_FQ,4) * (MSUM(COGS_FQ,4) / MLAG(MSUM(COGS_FQ,4),4)))] / MLAG(ASSETS_FQ,4)

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        return self.get_fiscal_unexp(
            src_field_prefix="PAYABLES",
            scale_field_prefix="COGS",
            denom_field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            src_aggr_op1y="msum",
            scale_aggr_op1y="msum",
            denom_aggr_op1y=None,
            fiscal_keyspace=fiscal_keyspace,
            freq=freq,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def UNEXP_AR(self, field, **kwds_args):
        """UNEXP_AR: UNEXPECTED RECEIVABLES
        See "Fundamental Information Analysis" by Lev & Thiagarajan (1993)
        or "Abnormal Returns to Fundamental Analysis Strategy" by Abarbanell & Bushee (1997)
        or "The Detection of Earnings Manipulation" by Beneish (1999)
        Prior: HIGH LEVEL = BEARISH
        ==> Growth in Accounts Recievables may reflect an aggressive revenue recognition policy (revenue inflation)
        Prior: HIGH LEVEL = BEARISH"""
        # DL:UNEXP_AR_FQ = [RECEIVABLES_FQ - (MLAG(RECEIVABLES_FQ,4) * (MSUM(SALES_FQ,4) / MLAG(MSUM(SALES_FQ,4),4)))] / MLAG(ASSETS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        return self.get_fiscal_unexp(
            src_field_prefix="RECEIVABLES",
            scale_field_prefix="SALES",
            denom_field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            src_aggr_op1y="msum",
            scale_aggr_op1y="msum",
            denom_aggr_op1y=None,
            fiscal_keyspace=fiscal_keyspace,
            freq=freq,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def UNEXP_SGA(self, field, **kwds_args):
        """UNEXP_SGA: UNEXPECTED SG&A EXPENSE
        See "Fundamental Information Analysis" by Lev & Thiagarajan (1993)
        or "Abnormal Returns to Fundamental Analysis Strategy" by Abarbanell & Bushee (1997)
        ----------------------------------------------------------------------
        Prior: HIGH LEVEL = BULLISH; LOW LEVEL = BEARISH [Note: Opposite logic/conclusion from A&B (1997)???]
            ==> Unexpectedly Low SG&A Changes (Low Factor Value) may represent Earnings Manipulation (Bad)
            ==> Opposite logic/conclusion from A&B (1997)???
        """
        # DL:UNEXP_SGA_FQ = [SGA_FQ - (MLAG(SGA_FQ,4) * (MSUM(SALES_FQ,4) / MLAG(MSUM(SALES_FQ,4),4)))] / MLAG(ASSETS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        return self.get_fiscal_unexp(
            src_field_prefix="SGA",
            scale_field_prefix="SALES",
            denom_field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            src_aggr_op1y="msum",
            scale_aggr_op1y="msum",
            denom_aggr_op1y=None,
            fiscal_keyspace=fiscal_keyspace,
            freq=freq,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def UNEXP_ACCR_LIAB(self, field, **kwds_args):
        """UNEXP_ACCR_LIAB: UNEXPECTED ACCRUED LIABILITIES"""
        # DL:UNEXP_ACCR_LIAB = [EXP_ACCRUED_FQ - (MLAG(EXP_ACCRUED_FQ,4) * (MSUM(SALES_FQ,4) / MLAG(MSUM(SALES_FQ,4),4)))] / MLAG(ASSETS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        return self.get_fiscal_unexp(
            src_field_prefix="EXP_ACCRUED",
            scale_field_prefix="SALES",
            denom_field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            src_aggr_op1y="msum",
            scale_aggr_op1y="msum",
            denom_aggr_op1y=None,
            fiscal_keyspace=fiscal_keyspace,
            freq=freq,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def UNEXP_DA(self, field, **kwds_args):
        """UNEXP_DA: UNEXPECTED DEPRECIATION & AMORTIZATION EXPENSE
        Prior: HIGH LEVEL = BEARISH
        High Unexpected D&A may reflect management's acceleration of D&A
        for (temporary/artificial/unsustainable) tax relief purposes
        """
        # DL:UNEXP_DA_FQ = [DA_FQ - (MLAG(DA_FQ,4) * (MSUM(PPE_GROSS_FQ,4) / MLAG(MSUM(PPE_GROSS_FQ,4),4)))] / MLAG(ASSETS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        return self.get_fiscal_unexp(
            src_field_prefix="DA",
            scale_field_prefix="PPE_GROSS",
            denom_field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            src_aggr_op1y="msum",
            scale_aggr_op1y="msum",
            denom_aggr_op1y=None,
            fiscal_keyspace=fiscal_keyspace,
            freq=freq,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def UNEXP_INV(self, field, **kwds_args):
        """UNEXP_INV: UNEXPECTED INVENTORY LEVELS
        See "Fundamental Information Analysis" by Lev & Thiagarajan (1993)
        or "Abnormal Returns to Fundamental Analysis Strategy" by Abarbanell & Bushee (1997)
        Prior: HIGH LEVEL = BEARISH
        ==> High level of (unexpected) inventory may represent weaker than expected sales and/or excessive risk taking by management
        ==> Opposite logic/conclusion from A&B (1997)???
        """
        # DL:UNEXP_INV_FQ = [INVENTORY_FQ - (MLAG(INVENTORY_FQ,4) * (MSUM(COGS_FQ,4) / MLAG(MSUM(COGS_FQ,4),4)))] / MLAG(ASSETS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        return self.get_fiscal_unexp(
            src_field_prefix="INVENTORY",
            scale_field_prefix="COGS",
            denom_field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            src_aggr_op1y="msum",
            scale_aggr_op1y="msum",
            denom_aggr_op1y=None,
            fiscal_keyspace=fiscal_keyspace,
            freq=freq,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def COGS2INV_ABSDIV1Y(self, field, **kwds_args):
        """COGS2INV_ABSDIV1Y: Absolute Value of Divergence in % Change over Past 4Q in COGS (Sum4Q) vs Inventory (Ave4Q)
        COGS2INV_ABSDIV1Y = ABS(MPCTCHG(MSUM(COGS_FQ,4),4) - MPCTCHG(MMEAN(INVENTORY_FQ,4),4))
        ==> High level of (unexpected) inventory may represent weaker than expected sales and/or excessive risk taking by management
        """
        # DL:COGS2INV_ABSDIV1Y = ABS(MPCTCHG(MSUM(COGS_FQ,4),4'pctchg'AN(INVENTORY_FQ,4),4))

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        # Note: Use of replace_missing_with_zero=True in request below...No inventory may be recorded as missing inventory value
        inv_mean1y_pctchg1y = self.get_fiscal_field(
            field_prefix="INVENTORY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=True,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        cogs_sum1y_pctchg1y = self.get_fiscal_field(
            field_prefix="COGS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (cogs_sum1y_pctchg1y - inv_mean1y_pctchg1y).absolute()
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def CFOPS2NI_ABSDIV1Y(self, field, **kwds_args):
        """CFOPS2NI_ABSDIV1Y: Absolute Value of Divergence in % Change over Past 4Q in Operating Cash Flow (Sum4Q) vs Net Income (Sum4Q)
        CFOPS2NI_ABSDIV1Y = ABS(MPCTCHG(MSUM(CFOPS_FQ,4),4) - MPCTCHG(MSUM(NI_FQ,4),4))
        Prior: HIGH LEVEL = BEARISH
        Consistent Variability between Cash Flows & Earnings is a possible indication of earnings manipulation
        """
        # DL:CFOPS2NI_ABSDIV4Q_FQ = ABS(MPCTCHG(MSUM(CFOPS_FQ,4),4) - MPCTCHG(MSUM(NI_FQ,4),4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        cfops_pctchg1y = self.get_fiscal_field(
            field_prefix="CFOPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        ni_pctchg1y = self.get_fiscal_field(
            field_prefix="NI",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (cfops_pctchg1y - ni_pctchg1y).absolute()
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def EBITDA2NI_ABSDIV1Y(self, field, **kwds_args):
        """EBITDA2NI_ABSDIV1Y: Absolute Value of Divergence in % Change over Past 4Q in EBITDA (Sum4Q) vs Net Income (Sum4Q)
        EBITDA2NI_ABSDIV1Y = ABS(MPCTCHG(MSUM(EBITDA_FQ,4),4) - MPCTCHG(MSUM(NI_FQ,4),4))
        Prior: HIGH LEVEL = BEARISH
        Consistent Variability between EBITDA & Earnings is a possible indication of earnings manipulation
        """
        # DL:EBITDA2NI_ABSDIV1Y = ABS(MPCTCHG(MSUM(EBITDA_FQ,4),4) - MPCTCHG(MSUM(NI_FQ,4),4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        ebitda_pctchg1y = self.get_fiscal_field(
            field_prefix="EBITDA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        ni_pctchg1y = self.get_fiscal_field(
            field_prefix="NI",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (ebitda_pctchg1y - ni_pctchg1y).absolute()
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def AR2SALES_DIV1Y(self, field, **kwds_args):
        """AR2SALES_DIV1Y: Divergence in % Change over Past 4Q Accounts Receivable (Ave4Q) vs Sales (Sum4Q)
        AR2SALES_DIV1Y = MPCTCHG(MMEAN(RECEIVABLES_FQ,4),4) - MPCTCHG(MSUM(SALES_FQ,4),4)
        Note: This factor formulation is opposite sign from formulation used in Arabanell & Bushee (1997)
        Prior: HIGH LEVEL = BEARISH
        ==> Higher Accounts Receivables Growth than Sales Growth (High Factor Value)
            may reflect an aggressive revenue recognition policy (artificial sales aka revenue inflation)
        """
        # DL:AR2SALES_DIV1Y = MPCTCHG(MMEAN(RECEIVABLES_FQ,4),4) - MPCTCHG(MSUM(SALES_FQ,4),4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        sales_sum1y_pctchg1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        ar_mean1y_pctchg1y = self.get_fiscal_field(
            field_prefix="RECEIVABLES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (
            ar_mean1y_pctchg1y - sales_sum1y_pctchg1y
        )  # <-- Note: No absolute value operator here! [since this factor is 'DEV' not 'ABSDEV']
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def SGA2SALES_DIV1Y(self, field, **kwds_args):
        """SGA2SALES_DIV1Y: Divergence in % Change over Past 4Q in Operating Cash Flow (Sum4Q) vs Net Income (Sum4Q)
        SGA2SALES_DIV1Y = MPCTCHG(MSUM(SGA_FQ,4)-MSUM(END_FQ,4),4) - MPCTCHG(MSUM(SALES_FQ,4),4)
        Note: This factor formulation is opposite sign from formulation used in Arabanell & Bushee (1997)
        Prior: HIGH LEVEL = BULLISH; LOW LEVEL = BEARISH
        ==> Low SG&A Changes relative to Sales Changes (Low Factor Value) may represent Earnings Manipulation (Bad)
        ==> Opposite logic/conclusion from A&B (1997)???"""
        # DL:SGA2SALES_DIV1Y = MPCTCHG(MSUM(SGA_FQ,4)-MSUM(RND_FQ,4),4) - MPCTCHG(MSUM(SALES_FQ,4),4)

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        sga_sum1y = self.get_fiscal_field(
            field_prefix="SGA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        rnd_sum1y = self.get_fiscal_field(
            field_prefix="RND",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        sga_minus_rnd_pctchg1y = (sga_sum1y - rnd_sum1y).mpctchg1d(
            periods=fiscal_ppy,
            keyspace=fiscal_keyspace,
        )
        sales_sum1y_pctchg1y = sales_sum1y.mpctchg1d(
            periods=fiscal_ppy,
            keyspace=fiscal_keyspace,
        )
        result = (
            sga_minus_rnd_pctchg1y - sales_sum1y_pctchg1y
        )  # <-- Note: No absolute value operator here! [Since this factor is 'DEV' not 'ABSDEV']
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def GP2SALES_DIV1Y(self, field, **kwds_args):
        """GP2SALES_DIV1Y: Divergence in % Change over Past 4Q in Gross Profit (Sum4Q) vs Sales (Sum4Q)
        GP2SALES_DIV1Y = MPCTCHG(MSUM(GP_FQ,4),4) - MPCTCHG(MSUM(SALES_FQ,4),4)
        See "Fundamental Information Analysis" by Lev & Thiagarajan (1993)
        or "Abnormal Returns to Fundamental Analysis Strategy" by Abarbanell & Bushee (1997)
        or "The Detection of Earnings Manipulation" by Beneish (1999)
        Prior: HIGH LEVEL = BULLISH"""
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        gp_sum1y_pctchg1y = self.get_fiscal_field(
            field_prefix="GP",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        sales_sum1y_pctchg1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (
            gp_sum1y_pctchg1y - sales_sum1y_pctchg1y
        )  # <-- Note: No absolute value operator here! [Since this factor is 'DEV' not 'ABSDEV']
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    # LABOR FORCE CHANGE FACTORS...
    # ------------------------------
    @RootLib.temp_frame()
    def EMP2ASSETS_DIV1Y(self, field, **kwds_args):
        """EMP2ASSETS_DIV1Y: Divergence in % Change over Past 4Q in # Employees vs Assets
        EMP2ASSETS_DIV1Y = MPCTCHG(EMPLOYEES_FQ) - MPCTCHG(ASSETS_FQ,4)
        see: "Predicting Material Accounting Misstatements" by Dechow et.al. (2011)
        PRIOR: HIGH LEVEL = BULLISH; LOW LEVEL = BEARISH
        ---------------------------------------
        Dechow calls this factor "Abnormal Change in Employees"
        and postulates a negative relationship with prices
        [Theory: Disproportionate reductions in # employees indicates earnings manipulation]
        """
        # DL:EMP2ASSETS_DIV1Y = [MPCTCHG(EMPLOYEES_FQ) - MPCTCHG(ASSETS_FQ,4)]

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        employees_pctchg1y = self.get_fiscal_field(
            field_prefix="EMPLOYEES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        assets_pctchg1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            fiscal_keyspace=fiscal_keyspace,
            replace_missing_with_zero=False,
            multi_year_window=1,
            multi_year_op="mpctchg",
            multi_year_pct_required=1.0,
            multi_year_ignore_missing=False,
            freq=None,
        )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (
            employees_pctchg1y - assets_pctchg1y
        )  # <-- Note: No absolute value operator here! [Since this factor is 'DEV' not 'ABSDEV']
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def SALES_PER_EMP_PCHG1Y(self, field, **kwds_args):
        """SALES_PER_EMP_PCHG1Y Trailing 4Q %Change in Sales/Employees (Rolling 4 Quarters)
        See "Fundamental Informataion Analysis" by Lev & Thiagarajan (1993)
        or "Abnormal Returns to Fundamental Analysis Strategy" by Abarbanell & Bushee (1997)
        or "Predicting Material Accounting Misstatements" by Dechow et.al. (2011)
        PRIOR: HIGH LEVEL = BEARISH; LOW LEVEL = BULLISH
        -----------------------------------------------------
        According to Dechow (2011), increases in sales/employees usually accompany
        a decrease in headcount which often represents earnings manipulation.
        Consistent with this hypothesis, Abarbanell & Bushee (1997) found a negative relationship
        (i.e., increases in sales/employees portends negative future earnings)"""
        # DL:SALES_PER_EMP_PCHG1Y = MPCTCHG(SALES_PER_EMP_FQ,4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="SALES_PER_EMP",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def PCT_SOFT(self, field, **kwds_args):
        """PCT_SOFT_FQ: % OF SOFT ASSET aka (SOFT ASSETS/ TOTAL ASSETS)
        PCT_SOFT_FQ = (ASSETS_FQ - PPE_NET_FQ - CASH_FQ) / ASSETS_FQ
        Prior: HIGH LEVEL = BEARISH
        (High %soft asset provides more management descretion and therefore more potential for earnings manipulation)
        See "Balance Sheet as an Earnings Management Constraint" by Barton & Simko (2002)
        """
        # DL:PCT_SOFT_FQ = (ASSETS_FQ - PPE_NET_FQ - CASH_FQ) / ASSETS_FQ
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        ppe_net = self.get_fiscal_field(
            field_prefix="PPE_NET",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_add", "right")
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require positive assets
        assets.conditional_nullify_inplace(assets < 0)

        result = (assets - ppe_net - cash) / assets
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def NOA_PCHG1Y(self, field, **kwds_args):
        """NOA_PCHG1Y = YoY (4Q) Pct Change Net Operating Assets
        Note: Numerator of NOA_PCHG1Y (i.e., NOA_FQ(Q)-NOA(Q-4)) is related to (a component of) XFIN
        see 'External Financing & Future Stock Returns' by Richardson & Sloan, 2003
        NOTE: Richardson & Sloan normalized numerator=MDIFF(NOA_FQ,4) by Total Assets (not Net Operating Assets as here)
        Prior: HIGH LEVEL = BEARISH (High Net External Financing is Bad)"""
        # DL:NOA_PCHG1Y = MPCTCHG(NOA_FQ,4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="NOA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    @RootLib.temp_frame()
    def INV2A_DIFF1Y(self, field, **kwds_args):
        """INV2A_DIFF1Y = MDIFF(INVENTORY/ASSETS,4)
        Note: INV2A_DIFF1Y is related to Lev & Thiagarajan factor,
              but should be more stable (better) than simple INV_PCHG4Q
        See "Fundamental Information Analysis" by Lev & Thiagarajan (1993)
        or "Abnormal Returns to Fundamental Analysis Strategy" by Abarbanell & Bushee (1997)
        or "Predicting Material Accounting Misstatements" by Dechow et.al. (2011)"""
        # FL:INV2A_DIFF1Y = MDIFF(INVENTORY_FQ / ASSETS_FQ, 4)

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        inv = self.get_fiscal_field(
            field_prefix="INVENTORY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        inv[inv.where_missing()] = (
            0.0  # <-- No inventory may be recorded as missing inventory value
        )

        # Require positive assets
        assets.conditional_nullify_inplace(assets < 0)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        inv2a = inv / assets

        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        inv2a_diff1y = inv2a.mdiff1d(periods=fiscal_ppy, keyspace=fiscal_keyspace)
        return (
            self.calendarize(inv2a_diff1y, freq=freq, add_frame=False)
            if freq is not None
            else inv2a_diff1y
        )

    @RootLib.temp_frame()
    def CASH_CYCLE_PCHG1Y(self, field, **kwds_args):
        """Cash Cycle %Change Past 1 Year (4 Quarters)"""
        # DL:CASH_CYCLE_PCHG1Y = MPCTCHG(CASH_CYCLE_FQ,4)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="CASH_CYCLE",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mpctchg",
            freq=freq,
        )

    # ========================= OPERATING EFFICIENCY / OPERATIONS MANAGEMENT FACTORS ==============================

    @RootLib.temp_frame()
    def DSO(self, field, **kwds_args):
        """DSO: Days sales outstanding (Rolling 4 Quarters)"""
        # DL:DSO_FQ = (365. * RECEIVABLES_FQ / MSUM(SALES_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        recv = self.get_fiscal_field(
            field_prefix="RECEIVABLES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (365.0 * recv) / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def DAYS_PAY(self, field, **kwds_args):
        """DAYS_PAY: Days Payables (Rolling 4 Quarters of Sales)"""
        # DL:DAYS_PAY_FQ = (365. * PAYABLES_FQ / MSUM(SALES_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        payables = self.get_fiscal_field(
            field_prefix="PAYABLES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (365.0 * payables) / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def DAYS_INV(self, field, **kwds_args):
        """DAYS_INV: Days Inventory (Rolling 4 Quarters)"""
        # DL:DAYS_INV_FQ = (365. * INVENTORY_FQ) / MSUM(COGS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Note: Using replace_missing_with_zero=True...No inventory may be recorded as missing inventory value
        inventory = self.get_fiscal_field(
            field_prefix="INVENTORY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        cogs_sum1y = self.get_fiscal_field(
            field_prefix="COGS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (365.0 * inventory) / cogs_sum1y
        RootLib().set_control("ignore_mult", False)
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def DAYS_PDINV(self, field, **kwds_args):
        """DAYS_PDINV: Days Paid Inventory (Rolling 4 Quarters)"""
        # DL:DAYS_PDINV_FQ = (365. * (INVENTORY_FQ - PAYABLES_FQ)) / MSUM(COGS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Chose to use replace_missing_with_zero=False because of 'ignore_add'=True below
        inventory = self.get_fiscal_field(
            field_prefix="INVENTORY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        payables = self.get_fiscal_field(
            field_prefix="PAYABLES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        cogs_sum1y = self.get_fiscal_field(
            field_prefix="COGS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (365.0 * (inventory - payables)) / cogs_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def CASH_CYCLE(self, field, **kwds_args):
        """CASH_CYCLE: CASH CYCLE (Rolling 4 Quarters)
        CASH CYCLE = (DSO + DAYS_PDINV) = 365*RECV/SALES + 365*(INVENTORY-PAYABLES)/COGS
        See "Cash-to-Cash is What Counts" by Peter Ward, 2004"""
        # DL:CASH_CYCLE_FQ = (DSO_FQ + DAYS_PDINV_FQ)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        dso = self.get_fiscal_field(
            field_prefix="DSO",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        days_pdinv = self.get_fiscal_field(
            field_prefix="DAYS_PDINV",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_add", True)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = dso + days_pdinv
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def SALES_PER_EMP(self, field, **kwds_args):
        """SALES_PER_EMP (Rolling 4 Quarters)"""
        # DL:SALES_PER_EMP_FQ = (SALES_SUM4Q_FQ / EMPLOYEES_FQ)

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        employees = self.get_fiscal_field(
            field_prefix="EMPLOYEES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = sales_sum1y / employees
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def ASSET_TURNOVER(self, field, **kwds_args):
        """ASSET_TURNOVER: (SALES_SUM4Q / ASSET_AVE4Q) (Rolling 4 Quarters)
        [Note: Asset Turnover is the reciprical of the Capital Intensity Ratio]"""
        # DL:ASSET_TURNOVER_FQ = MSUM(SALES_FQ,4) / MMEAN(ASSETS_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative assets_mean1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        assets_mean1y.conditional_nullify_inplace(assets_mean1y < 0)

        result = sales_sum1y / assets_mean1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def INV_TURNOVER(self, field, **kwds_args):
        """INV_TURNOVER: (Sales / (Average Inventory)) (Rolling 4 Quarters)"""
        # DL:ASSET_TURNOVER_FQ = MSUM(SALES_FQ,4) / MMEAN(INVENTORY_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        inventory_mean1y = self.get_fiscal_field(
            field_prefix="INVENTORY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative inventory_mean1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        inventory_mean1y.conditional_nullify_inplace(inventory_mean1y < 0)

        result = sales_sum1y / inventory_mean1y
        RootLib().set_control("ignore_mult", False)
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def EQUITY_TURNOVER(self, field, **kwds_args):
        """EQUITY_TURNOVER: (Sales / (Average Equity)) (Rolling 4 Quarters)"""
        # DL:EQUITY_TURNOVER_FQ = MSUM(SALES_FQ,4) / MMEAN(EQUITY_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        equity_mean1y = self.get_fiscal_field(
            field_prefix="EQUITY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative equity_mean1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        equity_mean1y.conditional_nullify_inplace(equity_mean1y < 0)

        result = sales_sum1y / equity_mean1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def IC_TURNOVER(self, field, **kwds_args):
        """IC_TURNOVER: (Sales / Invested Capital) (Rolling 4 Quarters)"""
        # DL:IC_TURNOVER_FQ = MSUM(SALES_FQ,4) / MMEAN(IC_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        ic_mean1y = self.get_fiscal_field(
            field_prefix="IC",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative ic_mean1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        ic_mean1y.conditional_nullify_inplace(ic_mean1y < 0)

        result = sales_sum1y / ic_mean1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def PPE_NET_TURNOVER(self, field, **kwds_args):
        """PPE_NET_TURNOVER: (Sales / (Average Net PPE)) (Rolling 4 Quarters)"""
        # DL:PPE_NET_TURNOVER_FQ = MSUM(SALES_FQ,4) / MMEAN(PPE_NET_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        ppe_net_mean1y = self.get_fiscal_field(
            field_prefix="PPE_NET",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative ppe_net_mean1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        ppe_net_mean1y.conditional_nullify_inplace(ppe_net_mean1y < 0)

        result = sales_sum1y / ppe_net_mean1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def NOA_TURNOVER(self, field, **kwds_args):
        """NOA_TURNOVER: (Sales / (Average Net Operating Assets)) (Rolling 4 Quarters)
        See "The Use of DuPont Analysis by Market Participants, Soliman (2007)"""
        # DL:NOA_TURNOVER_FQ = MSUM(SALES_FQ,4) / MMEAN(NOA_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        noa_mean1y = self.get_fiscal_field(
            field_prefix="NOA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative noa_mean1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        noa_mean1y.conditional_nullify_inplace(noa_mean1y < 0)

        result = sales_sum1y / noa_mean1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def WC2A(self, field, **kwds_args):
        """WC2A: (Working Capital / Assets)"""
        # DL:WC2A_FQ = (WC_FQ / ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        wc = self.get_fiscal_field(
            field_prefix="WC",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        # Require non-negative assets
        # (arguably should rarely happen,
        # but also guarding against bad data)
        assets.conditional_nullify_inplace(assets < 0)

        result = wc / assets
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def OVERHEAD2SALES(self, field, **kwds_args):
        """OVERHEAD2SALES: Overhead / Sales"""
        # DL:OVERHEAD2SALES_FQ = (MSUM(OPINC_FQ,4) - MSUM(DA_FQ,4) - MSUM(NIB4X_FQ,4) / MSUM(SALES_FQ,4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        opinc_sum1y = self.get_fiscal_field(
            field_prefix="OPINC",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        da_sum1y = self.get_fiscal_field(
            field_prefix="DA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        nib4x_sum1y = self.get_fiscal_field(
            field_prefix="NIB4X",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control("ignore_add", "right")
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        opinc_less_da_sum1y = (
            opinc_sum1y - da_sum1y
        )  # <-- opinc_sum1y must be non-missing, but OK if da_sum1y is missing
        RootLib().set_control("ignore_add", False)
        overhead = (
            opinc_less_da_sum1y - nib4x_sum1y
        )  # <-- opinc_less_da_sum1y & nib4x_sum1y must both be non-missing

        RootLib().set_control("ignore_mult", False)
        result = overhead / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def GP2A(self, field, **kwds_args):
        """GP2A: GP (Rolling 4 Quarters) / Total Assets"""
        # DL:GP2A = (MSUM(GP_FQ,4) / MMEAN(ASSETS_FQ,4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Set the environmental controls
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Perform computations
        gp_sum1y = self.get_fiscal_field(
            field_prefix="GP",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        assets_mean1y = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mmean",
            freq=None,
        )

        # Require non-negative assets_mean1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        assets_mean1y.conditional_nullify_inplace(assets_mean1y < 0)

        result = gp_sum1y / assets_mean1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def ADV2SALES(self, field, **kwds_args):
        """ADV2SALES_FQ aka Advertising Intensity
        ADV2SALES_FQ: ((MSUM(SGA_ADV_FQ,4) / MSUM(SALES_FQ,4))
        Note: This measure utilized in Mohanran's G-Score (see Mohanran, 2004)
        """
        # DL:ADV2SALES_FQ = ((MSUM(SGA_ADV_FQ,4) / MSUM(SALES_FQ,4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        adv_exp_sum1y = self.get_fiscal_field(
            field_prefix="SGA_ADV",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        adv2sales = adv_exp_sum1y / sales_sum1y
        RootLib().set_control("ignore_mult", False)
        return (
            self.calendarize(adv2sales, freq=freq, add_frame=False)
            if freq is not None
            else adv2sales
        )

    @RootLib.temp_frame()
    def RND2SALES(self, field, **kwds_args):
        """RND2SALES_FQ aka R&D Intensity
        RND2SALES_FQ: ((MSUM(RND_FQ,4) / MSUM(SALES_FQ,4))
        Note: This measure utilized in Mohanran's G-Score (see Mohanran, 2004)
        """
        # DL:RND2SALES_FQ = ((MSUM(RND_FQ,4) / MSUM(SALES_FQ,4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        rnd_sum1y = self.get_fiscal_field(
            field_prefix="RND",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        rnd2sales = rnd_sum1y / sales_sum1y
        RootLib().set_control("ignore_mult", False)
        return (
            self.calendarize(rnd2sales, freq=freq, add_frame=False)
            if freq is not None
            else rnd2sales
        )

    @RootLib.temp_frame()
    def INTEXP2DEBT(self, field, **kwds_args):
        """INTEXP2DEBT: Serves as a proxy for implied Interest Rate on Debt (Cost of Debt Capital)
        INTEXP2DEBT = (IntExp / Debt)"""
        # DL:INTEXP2DEBT_FQ = (MSUM(TOTNETOPINTEXP_FQ,4) / LTD_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        intexp_sum1y = self.get_fiscal_field(
            field_prefix="TOTNETOPINTEXP",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        ltd = self.get_fiscal_field(
            field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values on left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative ltd
        # (arguably should rarely happen,
        # but also guarding against bad data)
        ltd.conditional_nullify_inplace(ltd < 0)

        result = intexp_sum1y / ltd
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_SGA(self, field, **kwds_args):
        """MARGIN_SGA: SG&A margin (Rolling 4 Quarters)
        Prior: High Level = Bearish (High SG&A Expense)
        """
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        sga_sum1y = self.get_fiscal_field(
            field_prefix="SGA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = sga_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_GP(self, field, **kwds_args):
        """MARGIN_GP: Gross profit margin (Rolling 4 Quarters)
        Prior: High Level = Bullish (High Gross Profit Margins)
        """
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        gp_sum1y = self.get_fiscal_field(
            field_prefix="GP",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = gp_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_OPINC(self, field, **kwds_args):
        """MARGIN_OPINC: Operating income margin (Rolling 4 Quarters)
        Prior: High Level = Bullish (High Operating Profit Margins)
        See "The Use of DuPont Analysis by Market Participants, Soliman (2007)
        """
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        opinc_sum1y = self.get_fiscal_field(
            field_prefix="OPINC",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = opinc_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_EBITDA(self, field, **kwds_args):
        """MARGIN_EBITDA: EBITDA margin (Rolling 4 Quarters)"""
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ebitda_sum1y = self.get_fiscal_field(
            field_prefix="EBITDA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = ebitda_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_EBIT(self, field, **kwds_args):
        """MARGIN_EBIT: EBIT margin (Rolling 4 Quarters)"""
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ebit_sum1y = self.get_fiscal_field(
            field_prefix="EBIT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = ebit_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_PRETAXINC(self, field, **kwds_args):
        """MARGIN_PRETAXINC: Pre-tax income margin (Rolling 4 Quarters)"""
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        pretaxinc_sum1y = self.get_fiscal_field(
            field_prefix="PRETAXINC",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = pretaxinc_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_NIB4X(self, field, **kwds_args):
        """MARGIN_NIB4X: Net income margin
        before extraordinary items & preferred divs (Rolling 4 Quarters)"""
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        nib4x_sum1y = self.get_fiscal_field(
            field_prefix="NIB4X",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y (arguably should rarely happen, but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = nib4x_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_NI(self, field, **kwds_args):
        """MARGIN_NI: Net income margin (Rolling 4 Quarters)"""
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ni_sum1y = self.get_fiscal_field(
            field_prefix="NI",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = ni_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_NI_COMMON(self, field, **kwds_args):
        """MARGIN_NI_COMMON: Net income margin
        available to common shareholders (Rolling 4 Quarters)"""
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ni_common_sum1y = self.get_fiscal_field(
            field_prefix="NI_COMMON",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = ni_common_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_CF(self, field, **kwds_args):
        """MARGIN_CF: Cash flow margin (Rolling 4 Quarters)"""
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        cf_sum1y = self.get_fiscal_field(
            field_prefix="CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = cf_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def MARGIN_FCF(self, field, **kwds_args):
        """MARGIN_FCF: Free cash flow margin (Rolling 4 Quarters)"""
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        fcf_sum1y = self.get_fiscal_field(
            field_prefix="FCF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = fcf_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def NOPAT(self, field, **kwds_args):
        """
        Net Operating Profits After Tax (NOPAT)
        NOPAT = [(Net Income) + (Interest Expense)] * [1 - (Tax Rate)]
        """
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ni = self.get_fiscal_field(
            field_prefix="NI",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        intexp = self.get_fiscal_field(
            field_prefix="TOTNETOPINTEXP",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        # <-- Not strictly correct to use tax_rate, but thought this would be more stable as you can get funky behavior from expression: (taxes_sum1y/pretaxinc_sum1y)
        tax_rate = self.get_fiscal_field(
            field_prefix="TAX_RATE",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- Allow for missing values on right of +/- operator
        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        nopat = (ni + intexp) * (1.0 - tax_rate)
        return (
            self.calendarize(nopat, freq=freq, add_frame=False)
            if freq is not None
            else nopat
        )

    @RootLib.temp_frame()
    def MARGIN_NOPAT(self, field, **kwds_args):
        """MARGIN_NOPAT: NOPAT (Net Operating Profit After Taxes) Margin (Rolling 4 Quarters)"""
        # DL:MARGIN_NOPAT_FQ = [(MSUM(NI_FQ,4)+MSUM(TOTNETOPINTEXP_FQ,4))/MSUM(SALES_FQ,4)] x [1 - (MSUM(TAXES_FQ,4)/MSUM(PRETAXINC_FQ,4))]
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        nopat_sum1y = self.get_fiscal_field(
            field_prefix="NOPAT",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Will treat missing values in left or mult/div as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require non-negative sales_sum1y
        # (arguably should rarely happen,
        # but also guarding against bad data)
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        result = nopat_sum1y / sales_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    # ===================================== CAPITAL MANAGEMENT FACTORS =========================================

    @RootLib.temp_frame()
    def CAPACQ_RATIO(self, field, **kwds_args):
        """Capital Acquisition Ratio: (MSUM(CFOPS_FQ,4) - MSUM(-1.*CASHDIV_PD_CF_FQ,4)) / MSUM(-1*CFINV_FQ,4)
        Prior: High Capital Acquisition Level = Bullish"""
        # FL:CAPACQ_RATIO_FQ = (MSUM(CFOPS_FQ,4) - MSUM(-1.*CASHDIV_PD_CF_FQ,4)) / MSUM(-1.*CFINV_FQ,4)   NOTE: (CASHDIV_PD_CF_FQ < 0)    <-- USE IGNORE_ADD FOR DIVS ADD??
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        cfops_sum1y = self.get_fiscal_field(
            field_prefix="CFOPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # NOTE: (CASHDIV_PD_CF_FQ < 0)
        cashdiv_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CASHDIV_PD_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # NOTE: (CFINV_FQ < 0) FOR INVESTMENTS
        cfinv_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CFINV",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left"
        )  # <-- cfops_sum1y required to non-missing, cashdiv_sum1y can be missing
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = (cfops_sum1y - cashdiv_sum1y) / cfinv_sum1y
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def ABNORM_CAPINV(self, field, **kwds_args):
        """ABNORM_CAPINV: Abnormal Capital Investment
        Common wisdom is that high CapEx is good, but actuality is bad according to academic research & additional empirical tests
        Prior: High CapEx Level = Bearish (See Titman, Wei & Xie, 2004)"""
        # FL:ABNORM_CAPINV_FQ = (MSUM(CFINV_FQ,4) / MMEAN(MSUM(CFINV_FQ,4),12)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        cfinv_sum1y = self.get_fiscal_field(
            field_prefix="CFINV",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        cfinv_sum1y_mean3y = cfinv_sum1y.mmean1d(
            3 * fiscal_ppy,
            keyspace=fiscal_keyspace,
            pct_required=0.5,
            ignore_missing=True,
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require cfinv_sum1y_mean3y to be non-negative
        # (to allow use as denominator)
        cfinv_sum1y_mean3y.conditional_nullify_inplace(cfinv_sum1y_mean3y < 0)

        abnorm_capinv = cfinv_sum1y / cfinv_sum1y_mean3y
        return (
            self.calendarize(abnorm_capinv, freq=freq, add_frame=False)
            if freq is not None
            else abnorm_capinv
        )

    @RootLib.temp_frame()
    def SHARES_PCHG1Y(self, field, **kwds_args):
        """SHARES_PCHG4Q: (Shares / Shares(Q-4)) - 1"""
        # DL:SHARES_PCHG4Q_FQ = MPCTCHG(SHARES_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        shares_pctchg1y = self.get_fiscal_field(
            field_prefix="SHARES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mpctchg",
            freq=None,
        )
        return (
            self.calendarize(shares_pctchg1y, freq=freq, add_frame=False)
            if freq is not None
            else shares_pctchg1y
        )

    @RootLib.temp_frame()
    def EV_TREND1Y(self, field, **kwds_args):
        """EV_TREND1Y: ( (PRICE*SHARES + LTD + CURR_LTD - CASH) / (PRICE*SHARES(Q-4) + LTD(Q-4) + CURR_LTD(Q-4) - CASH(Q-4)) ) - 1"""
        # FL:EV_TREND4Q = ( ((Q2D(SHARES_FQ) * PRICE) + Q2D(LTD_FQ + CURR_LTD_FQ - CASH_FQ))
        #                 / ((Q2D(LAG(SHARES_FQ,4)) * PRICE) + Q2D(LAG((LTD_FQ + CURR_LTD_FQ - CASH_FQ),4))) ) - 1
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        # Procure fundamental components (in fiscal time)
        shares = self.get_fiscal_field(
            field_prefix="SHARES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        shares_lag1y = self.get_fiscal_field(
            field_prefix="SHARES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="shift",
            freq=None,
        )
        ltd = self.get_fiscal_field(
            field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_ltd = self.get_fiscal_field(
            field_prefix="CURR_LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        # Get closing price (in calendar time)
        # Use close fill 5D for daily (freq='WEEKDAY') case
        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        # Perform computations
        # ----------------------
        RootLib().set_control("ignore_add", True)
        debt_term = ltd + curr_ltd - cash
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        debt_term_lag1y = debt_term.shift1d(fiscal_ppy, keyspace=fiscal_keyspace)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- Need market value to be non-missing, but OK is debt_term is missing
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        # Recall, close is in calendar time/space, so output will be in calendar time/space
        ev_term_curr = (close * shares) + debt_term
        ev_term_prev = (close * shares_lag1y) + debt_term_lag1y

        ev_trend = (ev_term_curr / ev_term_prev) - 1
        return ev_trend

    @RootLib.temp_frame()
    def XFIN_CF(self, field, **kwds_args):
        """XFIN_CF = Net External Financing = [(Net Stock Issuance) + (Net LT & ST Debt Issuance) - (Cash Divs Paid)]
        XFIN_CF = [MSUM(NET_STK_ISSUANCE_CF_FQ,4) + MSUM(NET_DEBT_ISSUANCE_CF_FQ,4) - MSUM(-1.*CASHDIV_PD_CF_FQ,4)]   NOTE: (CASHDIV_PD_CF_FQ < 0)
        XFIN_CF Uses Statement of Cash Flow Formulation
        NET_DEBT_ISSUANCE_CF (RF Code:FPRD) incorporates NET changes in BOTH Short-Term & Long-Term debt Issuance/Retirement
        see 'External Financing & Future Stock Returns' by Richardson & Sloan, 2003
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR!!!
        Prior: HIGH LEVEL = BEARISH (High Net External Financing is Bad)"""
        # DL:XFIN_CF_FQ = [MSUM(NET_STK_ISSUANCE_CF_FQ,4) + MSUM(NET_DEBT_ISSUANCE_CF_FQ,4) - MSUM(-1.*CASHDIV_PD_CF_FQ,4)]
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # NOTE: (CASHDIV_PD_CF_FQ < 0)
        cash_divs_cf_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CASHDIV_PD_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        net_stock_issuance_cf_sum1y = self.get_fiscal_field(
            field_prefix="NET_STK_ISSUANCE_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        net_debt_issuance_cf_sum1y = self.get_fiscal_field(
            field_prefix="NET_DEBT_ISSUANCE_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        xfin_cf = (
            net_stock_issuance_cf_sum1y
            + net_debt_issuance_cf_sum1y
            - cash_divs_cf_sum1y
        )
        return (
            self.calendarize(xfin_cf, freq=freq, add_frame=False)
            if freq is not None
            else xfin_cf
        )

    @RootLib.temp_frame()
    def XFIN_BS(self, field, **kwds_args):
        """XFIN_BS = Net External Financing = [(Net Stock Issuance) + (Net LT & ST Debt Issuance) - (Cash Divs Paid)]
        XFIN_BS = [MDIFF(TOT_COM_STK_FQ,4) + MDIFF(TOT_PREF_STK_FQ,4) + MDIFF(STDEBT_FQ,4) + MDIFF(LTD_PURE_FQ,4)]
        XFIN_CF Uses Balance Sheet Formulation (Richardson & Sloan ignore Dividend effects in B/S formulation)
        [NOTE: RF Does not seem to allow break-out of convertible & non-convertible debt items as the academic paper suggests]
        see 'External Financing & Future Stock Returns' by Richardson & Sloan, 2003
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR!!!
        Prior: HIGH LEVEL = BEARISH (High Net External Financing is Bad)"""
        # DL:XFIN_BS_FQ = [MDIFF(TOT_COM_STK_FQ,4) + MDIFF(TOT_PREF_STK_FQ,4) + MDIFF(STDEBT_FQ,4) + MDIFF(LTD_PURE_FQ,4)]
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        com_stk_issuance_bs = self.get_fiscal_field(
            field_prefix="TOT_COM_STK",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mdiff",
            freq=None,
        )

        # TOT_PREF_STK_FQ is often missing when the value is intended to be zero
        pref_stk_issuance_bs = self.get_fiscal_field(
            field_prefix="TOT_PREF_STK",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mdiff",
            freq=None,
        )

        net_stdebt_issuance_bs = self.get_fiscal_field(
            field_prefix="STDEBT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mdiff",
            freq=None,
        )

        # Note: LTD_PURE_FQ Excludes Capital Leases from LTD_FQ.
        # Also, LTD_PURE_FQ is often missing when the value is intended to be zero
        net_ltdebt_issuance_bs = self.get_fiscal_field(
            field_prefix="LTD_PURE",
            alt_field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="mdiff",
            freq=None,
        )

        RootLib().set_control("ignore_add", True)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        xfin_bs = (
            com_stk_issuance_bs
            + pref_stk_issuance_bs
            + net_stdebt_issuance_bs
            + net_ltdebt_issuance_bs
        )
        return (
            self.calendarize(xfin_bs, freq=freq, add_frame=False)
            if freq is not None
            else xfin_bs
        )

    @RootLib.temp_frame()
    def XFIN_CF2NOA(self, field, **kwds_args):
        """XFIN_CF2NOA = [Net External Financing (Cash Flow Method) / Net Operating Assets (Trailing 4Q Average)]
        see 'External Financing & Future Stock Returns' by Richardson & Sloan, 2003
        NOTE: Richardson & Sloan normalized XFIN by Total Assets (not Net Operating Assets as here)
        Prior: HIGH LEVEL = BEARISH (High Net External Financing is Bad)"""
        # DL:XFIN_CF2NOA_FQ = (XFIN_CF_FQ / MMEAN(NOA_FQ,4))
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Note: XFIN_CF ALREADY INCORPORATES SUM1Y
        xfin_cf = self.get_fiscal_field(
            field_prefix="XFIN_CF",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        noa_mean1y = self.get_fiscal_field(
            field_prefix="NOA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mmean",
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require noa_mean1y to be non-negative
        # (for use as denominator below)
        noa_mean1y.conditional_nullify_inplace(noa_mean1y < 0)

        xfin_cf2noa = xfin_cf / noa_mean1y
        return (
            self.calendarize(xfin_cf2noa, freq=freq, add_frame=False)
            if freq is not None
            else xfin_cf2noa
        )

    @RootLib.temp_frame()
    def XFIN_BS2NOA(self, field, **kwds_args):
        """XFIN_BS2NOA = [Net External Financing (Balance Sheet Method) / Net Operating Assets]
        see 'External Financing & Future Stock Returns' by Richardson & Sloan, 2003
        NOTE: Richardson & Sloan normalized XFIN by Total Assets (not Net Operating Assets as here)
        Prior: HIGH LEVEL = BEARISH (High Net External Financing is Bad)"""
        # DL:XFIN_BS2NOA_FQ = (XFIN_BS_FQ / MMEAN(NOA_FQ,4))
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Note: XFIN_BS ALREADY INCORPORATES DIFF1Y
        xfin_bs = self.get_fiscal_field(
            field_prefix="XFIN_BS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        noa_mean1y = self.get_fiscal_field(
            field_prefix="NOA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mmean",
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require noa_mean1y to be non-negative
        # (for use as denominator below)
        noa_mean1y.conditional_nullify_inplace(noa_mean1y < 0)

        xfin_bs2noa = xfin_bs / noa_mean1y
        return (
            self.calendarize(xfin_bs2noa, freq=freq, add_frame=False)
            if freq is not None
            else xfin_bs2noa
        )

    @RootLib.temp_frame()
    def CAPEX2A(self, field, **kwds_args):
        """CAPEX2A_FQ = (CapEx / Assets)
        [Here: CapEx from Cash Flow Statement]
        This factor is sometimes referred to as 'CapEx Intensity'
        Is used as one of the components of Monhanran, G-Score (2004)
        Prior: HIGH LEVEL = BULLISH
        Common wisdom is that high CapEx is Good for Future Growth,
        but in actuality is bad according to some academic research & our backtests
        Prior: LEVEL = BEARISH (See "Capital Investments & Stock Returns" by Titman, Wei & Xie, 2004) contradicts Monhanran (2004)
        """
        # DL:CAPEX2A_FQ = (MSUM(-1.*CAPEX_CF_FQ,4) / ASSETS_FQ)  NOTE: (CAPEX_CF_FQ < 0)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # NOTE: (CAPEX_CF_FQ < 0)
        # Note: No capex may be provided as missing records
        capex_cf_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CAPEX_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # assets must be non-negative here
        assets.conditional_nullify_inplace(assets < 0)

        capex2a = capex_cf_sum1y / assets
        return (
            self.calendarize(capex2a, freq=freq, add_frame=False)
            if freq is not None
            else capex2a
        )

    @RootLib.temp_frame()
    def CAPEX2SALES(self, field, **kwds_args):
        """CAPEX2SALES_FQ = MSUM(-1.*CAPEX_CF_FQ,4)/MSUM(SALES_FQ,4)
        [Here: CapEx from Cash Flow Statement]
        Note: This measure utilized in Mohanran's G-Score (see Mohanran, 2004)
        """
        # FL:CAPEX2SALES_FQ = (MSUM(-1.*CAPEX_CF_FQ,4) / MSUM(SALES_FQ,4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # NOTE: (CAPEX_CF_FQ < 0)
        # Note: No capex may be provided as missing records
        capex_cf_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CAPEX_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # sales_sum1y must be non-negative here
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        capex2sales = capex_cf_sum1y / sales_sum1y
        return (
            self.calendarize(capex2sales, freq=freq, add_frame=False)
            if freq is not None
            else capex2sales
        )

    @RootLib.temp_frame()
    def CAPEX2SALES_DIFF1Y(self, field, **kwds_args):
        """CAPEX2SALES_DIFF1Y = MDIFF(MSUM(CAPEX_FQ,4)/MSUM(SALES_FQ,4),4) [Here: CapEx from Cash Flow Statement]
        Note: CAPEX2SALES_DIFF1Y is related to Lev & Thiagarajan factor,
              but should be more stable (better) than simple CAPEX_PCHG4Q
        -----------------------------------------------------------------
        Prior: HIGH LEVEL = BEARISH
        [Somewhat counter-intuitive, but empirical evidence shows that firms tend to over-invest
        and/or market does not credit firms with CapEx spending [per findings in Abarbanell & Bushee (1997)]
        Note: Similar to Abnormal Capital Investment (ABNORM_CAPINV_FQ)
        -----------------------------------------------------------------
        See "Fundamental Information Analysis" by Lev & Thiagarajan (1993)
        or "Abnormal Returns to Fundamental Analysis Strategy" by Abarbanell & Bushee (1997)
        """
        # DL:CAPEX2SALES_DIFF1Y_FQ = [MDIFF(MSUM(-1.*CAPEX_CF_FQ,4) / MSUM(SALES_FQ,4),4)]  NOTE: (CAPEX_CF_FQ < 0)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        return self.get_fiscal_field(
            field_prefix="CAPEX2SALES",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=freq,
        )

    @RootLib.temp_frame()
    def DA2CAPEX_ABSDIV1Y(self, field, **kwds_args):
        """DA2CAPEX_ABSDIV1Y: Absolute Value of Divergence in % Change over Past 4Q in
                                Depreciation & Amortization (Sum4Q) vs Cap Expenditures (Sum4Q)
        DA2CAPEX_ABSDIV1Y = ABS(MPCTCHG(MSUM(DA_CF_FQ,4),4) - MPCTCHG(MSUM(-1.*CAPEX_CF_FQ,4),4))  NOTE: (CAPEX_CF_FQ < 0)
        -----------------------------------------------------------------
        Prior: HIGH LEVEL = BEARISH (All Deviations are Bad)
        Theory: Low DA2CAPEX Deviations: Firms are Under-Investing, High DA2CAPEX Deviations: Firms are Over-Expanding]
        """
        # DL:DA2CAPEX_ABSDIV4Q_FQ = [ABS(MPCTCHG(MSUM(DA_CF_FQ,4),4) - MPCTCHG(MSUM(-1.*CAPEX_CF_FQ,4),4))]  NOTE: (CAPEX_CF_FQ < 0)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # Note: No da may be provided as missing records
        da_sum1y_pctchg1y = self.get_fiscal_field(
            field_prefix="DA_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            multi_year_window=1,
            multi_year_op="mpctchg",
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        # NOTE: (CAPEX_CF_FQ < 0)
        # Note: No capex may be provided as missing records
        capex_cf_sum1y_pctchg1y = -1.0 * self.get_fiscal_field(
            field_prefix="CAPEX_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            multi_year_window=1,
            multi_year_op="mpctchg",
            freq=None,
        )

        result = (da_sum1y_pctchg1y - capex_cf_sum1y_pctchg1y).absolute()
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    # ============================== SOLVENCY / BALANCE SHEET FACTORS ==================================

    @RootLib.temp_frame()
    def L2A(self, field, **kwds_args):
        """L2A =(Liabilities / Assets)"""
        # DL:L2A_FQ = (LIAB_FQ / ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # NOTE: (CAPEX_CF_FQ < 0)
        # Note: No capex may be provided as missing records
        liab = self.get_fiscal_field(
            field_prefix="LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # assets must be non-negative here
        assets.conditional_nullify_inplace(assets < 0)

        l2a = liab / assets
        return (
            self.calendarize(l2a, freq=freq, add_frame=False)
            if freq is not None
            else l2a
        )

    @RootLib.temp_frame()
    def MKTCAP(self, field, **kwds_args):
        """MKTCAP: Market Value (Market Cap)
        For freq='WEEKDAY', applies fill1d for 5 Days for prc_lib['CLOSE_D']
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        mv = None  # <-- Initialization

        # First, see if MKTCAP exists in prc_lib
        if freq in AlphaLib.freq2suffix:
            prc_field = f"MKTCAP{AlphaLib.freq2suffix[freq]}"
            if prc_field in RootLib()[prc_lib].fields():
                mv = self.get_calendarized_field(
                    field_prefix="MKTCAP",
                    freq=freq,
                    lib=prc_lib,
                    tfill_method_dict={"WEEKDAY": "pad"},
                    tfill_max_dict={"WEEKDAY": 5},
                )

        # Otherwise, build MKTCAP from (shares * close)
        if mv is None:
            cft_lib = self.get_property("cft_lib", field, grace=False)
            fiscal_mode = self.get_property(
                "fiscal_mode", field, grace=True, default_property_value="FQ"
            )
            if freq is not None:
                RootLib().set_control("freq", freq)

            close = self.get_calendarized_field(
                field_prefix="CLOSE",
                freq=freq,
                lib=prc_lib,
                tfill_method_dict={"WEEKDAY": "pad"},
                tfill_max_dict={"WEEKDAY": 5},
            )
            # CFT Convention: SHARES provided in Millions
            shares = self.get_fiscal_field(
                field_prefix="SHARES",
                fiscal_mode=fiscal_mode,
                lib=cft_lib,
                aggr_op1y=None,
                freq=freq,
            )
            RootLib().set_control("ignore_mult", False)
            RootLib().set_control("auto_compress", True)
            RootLib().set_control("variate_mode", "uni")
            mv = close * shares

        return mv

    @RootLib.temp_frame()
    def MVTA(self, field, **kwds_args):
        """MVTA: Market Value of Total Assets
        Used on Distress Measures: Campbell, Hilscher & Szilagyi, 2005
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR"""
        # DL:MVTA = MKTCAP + Q2D(LIAB_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        liab = self.get_fiscal_field(
            field_prefix="LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=freq,
        )
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        RootLib().set_control("ignore_add", "right")  # <-- Require mv to be non-missing
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return mv + liab

    @RootLib.temp_frame()
    def L2MVTA(self, field, **kwds_args):
        """L2MVTA_FQ =(Liabilities / Market Value of Total Assets)
        Used on Distress Measures: Campbell, Hilscher & Szilagyi, 2005"""
        # FL:L2MVTA_FQ = (LIAB/ MVTA)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        liab = self.get_fiscal_field(
            field_prefix="LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=freq,
        )
        mvta = self.get_calendarized_field(field_prefix="MVTA", freq=freq, lib=self)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return liab / mvta

    @RootLib.temp_frame()
    def ADJ_ASSETS(self, field, **kwds_args):
        """ADJ_ASSETS = (TOTAL ASSETS + (0.1 * (EQUITY - MKTCAP)))
        Used on Distress Measures: Campbell, Hilscher & Szilagyi, 2005
        NOTE: THIS IS NON-NORMALIZED ($ UNITS) (HELPER) FACTOR"""
        # DL:ADJ_ASSETS = (Q2D(ASSETS_FQ) + (0.1 * (Q2D(EQUITY_FQ) - MKTCAP)))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        equity = self.get_fiscal_field(
            field_prefix="EQUITY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=freq,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=freq,
        )
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        RootLib().set_control(
            "ignore_add", False
        )  # <-- Require both equity & mv & assets to be non-missing
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        adj_assets = assets + 0.1 * (equity - mv)
        return adj_assets

    @RootLib.temp_frame()
    def L2AA(self, field, **kwds_args):
        """Liability to Adjusted Assets
        LIAB2AA = (Q2D(LIAB) / ADJ_ASSETS) = (Q2D(LIAB) / (Q2D(ASSETS) + 0.1*(EQUITY-MKTCAP)))
        Used on Distress Measures: Campbell, Hilscher & Szilagyi, 2005"""
        # FL:L2AA = (Q2D(LIAB) / ADJ_ASSETS) = (Q2D(LIAB) / (Q2D(ASSETS) + 0.1*(EQUITY-MKTCAP)))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        liab = self.get_fiscal_field(
            field_prefix="LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=freq,
        )
        adj_assets = self.get_calendarized_field(
            field_prefix="ADJ_ASSETS", freq=freq, lib=self
        )

        # adj_assets must be non-negative here
        adj_assets.conditional_nullify_inplace(adj_assets < 0)

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return liab / adj_assets

    @RootLib.temp_frame()
    def CASH2MVTA(self, field, **kwds_args):
        """Cash to Market Value of Total Assets
        CASH2MVTA = (Q2D(CASH_FQ) / MVTA) = (Q2D(CASH_FQ) / (MKTCAP + Q2D(LIAB_FQ)))
        Used on Distress Measures: Campbell, Hilscher & Szilagyi, 2005"""
        # FL:CASH2MVTA = (Q2D(CASH) / MVTA) = = (Q2D(CASH_FQ) / (MKTCAP + Q2D(LIAB_FQ)))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=freq,
        )
        mvta = self.get_calendarized_field(field_prefix="MVTA", freq=freq, lib=self)

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return cash / mvta

    @RootLib.temp_frame()
    def LTD2A(self, field, **kwds_args):
        """LTD2A = (Long Term Debt / Assets)"""
        # DL:LTD2A_FQ = (LTD_FQ / ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ltd = self.get_fiscal_field(
            field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # assets must be non-negative here
        assets.conditional_nullify_inplace(assets < 0)

        ltd2a = ltd / assets
        return (
            self.calendarize(ltd2a, freq=freq, add_frame=False)
            if freq is not None
            else ltd2a
        )

    @RootLib.temp_frame()
    def DEBT2A(self, field, **kwds_args):
        """DEBT2A = (Debt / Assets)"""
        # DL:DEBT2A_FQ = ((LTD_FQ + CURR_LTD_FQ) / ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ltd = self.get_fiscal_field(
            field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_ltd = self.get_fiscal_field(
            field_prefix="CURR_LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", True
        )  # <-- Allow for ltd OR curr_ltd to be missing
        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # assets must be non-negative here
        assets.conditional_nullify_inplace(assets < 0)

        debt = ltd + curr_ltd
        debt2a = debt / assets
        return (
            self.calendarize(debt2a, freq=freq, add_frame=False)
            if freq is not None
            else debt2a
        )

    @RootLib.temp_frame()
    def ASSET_LOW_QUALITY(self, field, **kwds_args):
        """ASSET_LOW_QUALITY (as defined here) represents ratio of Non-Current, Non-Fixed Assets to all assets
        ----------------------------------------------------------------
        Traditionally, this factor represent the basis for the "AssetQualityIndex"
        which is nominally defined a the current value of this factor
        divided by the value four (fiscal) quarters ago.
        In actuality, this factor actually reflects LOW QUALITY ASSETS
        (logic being that Current & Fixed Assets are more valuable as they are more operationally important)
        As such, I have chosen to rename this factor ASSET_LOW_QUALITY_FQ accordingly.
        ----------------------------------------------------------------
        In this light, the prior expectations take the following stance...
        Prior: HIGH VALUE: BEARISH (Many Low Quality Assets are Less Valuable)"""
        # FL:ASSET_LOW_QUALITY_FQ = ((ASSETS_FQ - CURR_ASSETS_FQ - PPE_NET_FQ) / ASSETS_FQ) = ((NON_CURR_ASSETS_FQ - PPE_NET_FQ) / ASSETS_FQ)
        # FL:ASSET_LOW_QUALITY_FQ = (1 - (CURR_ASSETS_FQ - PPE_NET_FQ)/ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        curr_assets = self.get_fiscal_field(
            field_prefix="CURR_ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        ppe_net = self.get_fiscal_field(
            field_prefix="PPE_NET",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- Need assets to be non-missing, but OK if curr_assets OR ppe_net is missing
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # assets must be non-negative here
        assets.conditional_nullify_inplace(assets < 0)

        asset_low_quality = (assets - curr_assets - ppe_net) / assets
        return (
            self.calendarize(asset_low_quality, freq=freq, add_frame=False)
            if freq is not None
            else asset_low_quality
        )

    @RootLib.temp_frame()
    def NOA2A(self, field, **kwds_args):
        """NOA2A = (Net Operating Assets / Assets)"""
        # FL:NOA2A_FQ = (NOA_FQ / ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        noa = self.get_fiscal_field(
            field_prefix="NOA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # assets must be non-negative here
        assets.conditional_nullify_inplace(assets < 0)

        noa2a = noa / assets
        return (
            self.calendarize(noa2a, freq=freq, add_frame=False)
            if freq is not None
            else noa2a
        )

    @RootLib.temp_frame()
    def CASH2CURR_LIAB(self, field, **kwds_args):
        """CASH2CURR_LIAB = (Cash / Current Liabilities)"""
        # FL:CASH2CURR_LIAB_FQ = (CASH_FQ / CURR_LIAB_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        # NOTE: (CAPEX_CF_FQ < 0)
        # Note: No capex may be provided as missing records
        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_liab = self.get_fiscal_field(
            field_prefix="CURR_LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # curr_liab must be non-negative here (probably not necessary)
        curr_liab.conditional_nullify_inplace(curr_liab < 0)

        cash2curr_liab = cash / curr_liab
        return (
            self.calendarize(cash2curr_liab, freq=freq, add_frame=False)
            if freq is not None
            else cash2curr_liab
        )

    @RootLib.temp_frame()
    def CASH2SALES(self, field, **kwds_args):
        """CASH2SALES = (Cash / Sales)"""
        # FL:CASH2SALES_FQ = (CASH_FQ / MSUM(SALES_FQ,4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # sales_sum1y must be non-negative here
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        cash2sales = cash / sales_sum1y
        return (
            self.calendarize(cash2sales, freq=freq, add_frame=False)
            if freq is not None
            else cash2sales
        )

    @RootLib.temp_frame()
    def CURR_RATIO(self, field, **kwds_args):
        """Current Ratio = Current Assets / Current Liabilities"""
        # FL:CURR_RATIO_FQ = (CURR_ASSETS_FQ / CURR_LIAB_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        curr_assets = self.get_fiscal_field(
            field_prefix="CURR_ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_liab = self.get_fiscal_field(
            field_prefix="CURR_LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Require both curr_assets & curr_liab to be non-missing
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # curr_liab must be non-negative here (probably not necessary)
        curr_liab.conditional_nullify_inplace(curr_liab < 0)

        curr_ratio = curr_assets / curr_liab
        return (
            self.calendarize(curr_ratio, freq=freq, add_frame=False)
            if freq is not None
            else curr_ratio
        )

    @RootLib.temp_frame()
    def QUICK_RATIO(self, field, **kwds_args):
        """Quick Ratio = ((Current Assets - Inventory) / Current Liabilities)"""
        # FL:QUICK_RATIO_FQ = ((CURR_ASSETS_FQ - INVENTORY_FQ) / CURR_LIAB_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        curr_assets = self.get_fiscal_field(
            field_prefix="CURR_ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        inv = self.get_fiscal_field(
            field_prefix="INVENTORY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_liab = self.get_fiscal_field(
            field_prefix="CURR_LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- Allow for inv to be missing, but curr_assets must be non-missing
        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Require both curr_assets & curr_liab to be non-missing
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # curr_liab must be non-negative here (probably not necessary)
        curr_liab.conditional_nullify_inplace(curr_liab < 0)

        quick_ratio = (curr_assets - inv) / curr_liab
        return (
            self.calendarize(quick_ratio, freq=freq, add_frame=False)
            if freq is not None
            else quick_ratio
        )

    @RootLib.temp_frame()
    def FLOW_RATIO(self, field, **kwds_args):
        """Flow Ratio = ((Current Assets - Cash) / (Current Liabilities - ST Debt)"""
        # FL:FLOW_RATIO_FQ = ((CURR_ASSETS_FQ - CASH_FQ) / (CURR_LIAB_FQ - STDEBT_FQ))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        curr_assets = self.get_fiscal_field(
            field_prefix="CURR_ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_liab = self.get_fiscal_field(
            field_prefix="CURR_LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        stdebt = self.get_fiscal_field(
            field_prefix="STDEBT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- Allow for cash or stdebt to be missing, but curr_assets and curr_liab must be non-missing
        RootLib().set_control(
            "ignore_mult", False
        )  # <-- Require both numeratro & denominator to be non-missing
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # curr_liab must be non-negative here (probably not necessary)
        curr_liab.conditional_nullify_inplace(curr_liab < 0)

        flow_ratio = (curr_assets - cash) / (curr_liab - stdebt)
        return (
            self.calendarize(flow_ratio, freq=freq, add_frame=False)
            if freq is not None
            else flow_ratio
        )

    @RootLib.temp_frame()
    def NET_DEBT_RATIO(self, field, **kwds_args):
        """Net Debt Ratio"""
        # FL:NET_DEBT_RATIO_FQ = ((LTD_FQ + CURR_LTD_FQ + STDEBT_EX_CURR_LTD_FQ - CASH_FQ) / (LTD_FQ + CURR_LTD_FQ + STDEBT_EX_CURR_LTD_FQ - CASH_FQ + TOT_PREF_STK_FQ + TOT_COM_STK_FQ))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ltd = self.get_fiscal_field(
            field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_ltd = self.get_fiscal_field(
            field_prefix="CURR_LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        stdebt_ex_curr_ltd = self.get_fiscal_field(
            field_prefix="STDEBT_EX_CURR_LTD",
            alt_field_prefix="STDEBT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        pref_stk = self.get_fiscal_field(
            field_prefix="TOT_PREF_STK",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        com_stk = self.get_fiscal_field(
            field_prefix="TOT_COM_STK",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        RootLib().set_control("ignore_add", True)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        net_debt_ratio = (ltd + curr_ltd + stdebt_ex_curr_ltd - cash) / (
            ltd + curr_ltd + stdebt_ex_curr_ltd - cash + pref_stk + com_stk
        )
        return (
            self.calendarize(net_debt_ratio, freq=freq, add_frame=False)
            if freq is not None
            else net_debt_ratio
        )

    @RootLib.temp_frame()
    def CURRA2A(self, field, **kwds_args):
        """CURRA2A = (Current Assets / Assets)"""
        # FL:CURRA2A_FQ = (CURR_ASSETS_FQ / ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        curr_assets = self.get_fiscal_field(
            field_prefix="CURR_ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # assets must be non-negative here (probably not necessary)
        assets.conditional_nullify_inplace(assets < 0)

        curr_assets2a = curr_assets / assets
        return (
            self.calendarize(curr_assets2a, freq=freq, add_frame=False)
            if freq is not None
            else curr_assets2a
        )

    @RootLib.temp_frame()
    def NET_CURRA2A(self, field, **kwds_args):
        """NET_CURRA2A = (Net Current Assets / Assets)"""
        # FL:NET_CURRA2A_FQ = ((CURR_ASSETS_FQ - CURR_LIAB_FQ) / ASSETS_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        curr_assets = self.get_fiscal_field(
            field_prefix="CURR_ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_liab = self.get_fiscal_field(
            field_prefix="CURR_LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- No current debt may be recorded as missing current debt value
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # assets must be non-negative here (probably not necessary)
        assets.conditional_nullify_inplace(assets < 0)

        net_curr_assets2a = (curr_assets - curr_liab) / assets
        return (
            self.calendarize(net_curr_assets2a, freq=freq, add_frame=False)
            if freq is not None
            else net_curr_assets2a
        )

    @RootLib.temp_frame()
    def CASHBURN(self, field, **kwds_args):
        """Cash Burn Rate"""
        # FL:CASHBURN_FQ = (MSUM(CFINV_FQ,4) - MSUM(CFOPS_FQ,4)) / CASH_FQ
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        cfinv_sum1y = self.get_fiscal_field(
            field_prefix="CFINV",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        cfops_sum1y = self.get_fiscal_field(
            field_prefix="CFOPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # cash must be non-negative here (probably not necessary)
        cash.conditional_nullify_inplace(cash < 0)

        cashburn = (cfinv_sum1y - cfops_sum1y) / cash
        return (
            self.calendarize(cashburn, freq=freq, add_frame=False)
            if freq is not None
            else cashburn
        )

    @RootLib.temp_frame()
    def DEBT_COV(self, field, **kwds_args):
        """Debt Coverage Ratio
        DEBT_COV = (DISCRETONARY_PRETAX_INCOME) / (TOTAL DEBT)
                 = (EBITDA - CASH_DIV) / (STDEBT_EX_CURR_LTD + CURR_LTD + LTD)
        """
        # FL:DEBT_COV_FQ = (MSUM(EBITDA_FQ,4) - MSUM(-1.*CASHDIV_PD_CF_FQ,4)) / (STDEBT_EX_CURR_LTD_FQ + CURR_LTD_FQ + LTD_FQ)      NOTE: (CASHDIV_PD_CF_FQ < 0)   <-- USE IGNORE_ADD FOR DIVS ADD??
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ebitda_sum1y = self.get_fiscal_field(
            field_prefix="EBITDA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        # NOTE: (CASHDIV_PD_CF_FQ < 0)
        cashdiv_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CASHDIV_PD_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        stdebt_ex_curr_ltd = self.get_fiscal_field(
            field_prefix="STDEBT_EX_CURR_LTD",
            alt_field_prefix="STDEBT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_ltd = self.get_fiscal_field(
            field_prefix="CURR_LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        ltd = self.get_fiscal_field(
            field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- Require ebitda_sum1y to be non-missing, but OK if cashdiv_sum1y is missing
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        discretionary_pretax_income = ebitda_sum1y - cashdiv_sum1y

        RootLib().set_control(
            "ignore_add", True
        )  # <-- OK if some components of tot_debt are missing
        total_debt = stdebt_ex_curr_ltd + curr_ltd + ltd

        RootLib().set_control(
            "ignore_mult", "right_epsilon"
        )  # <-- Will treat missing values in right of mult/div operator as epsilon (but requires left component to be non-missing)
        # Use of 'right_epsilon' for division is helpful for yieldings a large (but non-missing) value that will preserve participation in subsequent rankings

        # tot_debt must be non-negative here (probably not necessary)
        total_debt.conditional_nullify_inplace(total_debt < 0)

        debt_cov = discretionary_pretax_income / total_debt

        return (
            self.calendarize(debt_cov, freq=freq, add_frame=False)
            if freq is not None
            else debt_cov
        )

    @RootLib.temp_frame()
    def INT_COV(self, field, **kwds_args):
        """Interest Coverage Ratio
        INT_COV = (DISCRETONARY_PRETAX_INCOME) / (INTEREST EXPENSE)
                 = (EBITDA - CASH_DIV) / (INTEREST EXPENSE)
        """
        # FL:INT_COV_FQ = (MSUM(EBITDA_FQ,4) - MSUM(-1.*CASHDIV_PD_CF_FQ,4)) / MSUM(TOTNETOPINTEXP_FQ,4)   NOTE: (CASHDIV_PD_CF_FQ < 0)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ebitda_sum1y = self.get_fiscal_field(
            field_prefix="EBITDA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        # NOTE: (CASHDIV_PD_CF_FQ < 0)
        cashdiv_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CASHDIV_PD_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        intexp_sum1y = self.get_fiscal_field(
            field_prefix="TOTNETOPINTEXP",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        stdebt_ex_curr_ltd = self.get_fiscal_field(
            field_prefix="STDEBT_EX_CURR_LTD",
            alt_field_prefix="STDEBT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_ltd = self.get_fiscal_field(
            field_prefix="CURR_LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        ltd = self.get_fiscal_field(
            field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- Require ebitda_sum1y to be non-missing, but OK if cashdiv_sum1y is missing
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        discretionary_pretax_income = ebitda_sum1y - cashdiv_sum1y

        RootLib().set_control(
            "ignore_mult", "right_epsilon"
        )  # <-- Will treat missing values in right of mult/div operator as epsilon (but requires left component to be non-missing)
        # Use of 'right_epsilon' for division is helpful for yieldings a large (but non-missing) value that will preserve participation in subsequent rankings
        int_cov = discretionary_pretax_income / intexp_sum1y

        return (
            self.calendarize(int_cov, freq=freq, add_frame=False)
            if freq is not None
            else int_cov
        )

    @RootLib.temp_frame()
    def CASH_DIV_COV(self, field, **kwds_args):
        """CASH_DIV_COV: Cash Dividend Coverage Ratio
        CASH_DIV_COV = Cash Flow (Sum 4Q) / Dividend (Sum 4Q)
        Indicates whether cash flow is sufficient to cover cash dividends
        Prior: HIGH LEVEL = BULLISH (Low Burden Cash Dividend)"""
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ni_cf_sum1y = self.get_fiscal_field(
            field_prefix="NI_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        da_cf_sum1y = self.get_fiscal_field(
            field_prefix="DA_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        # NOTE: (CASHDIV_PD_CF_FQ < 0)
        cashdiv_sum1y = -1.0 * self.get_fiscal_field(
            field_prefix="CASHDIV_PD_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- Require ni_cf_sum1y to be non-missing, but OK if da_cf_sum1y is missing
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        income_before_da = ni_cf_sum1y + da_cf_sum1y

        RootLib().set_control(
            "ignore_mult", "right_epsilon"
        )  # <-- Will treat missing values in right of mult/div operator as epsilon (but requires left component to be non-missing)
        # Use of 'right_epsilon' for division is helpful for yieldings a large (but non-missing) value that will preserve participation in subsequent rankings
        div_cov = income_before_da / cashdiv_sum1y

        return (
            self.calendarize(div_cov, freq=freq, add_frame=False)
            if freq is not None
            else div_cov
        )

    @RootLib.temp_frame()
    def EBITDA2CURR_LIAB(self, field, **kwds_args):
        """EBITDA2CURR_LIAB = (EBITDA / Current Liabilities)
        Prior: HIGH LEVEL = BULLISH (EBITDA supports a given Current Debt Level)
        """
        # DL:EBITDA2CURR_LIAB_FQ = (MSUM(EBITDA_FQ,4) / CURR_LIAB_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ebitda_sum1y = self.get_fiscal_field(
            field_prefix="EBITDA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        curr_liab = self.get_fiscal_field(
            field_prefix="CURR_LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "right_epsilon"
        )  # <-- Will treat missing values in right of mult/div operator as epsilon (but requires left component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        # Use of 'right_epsilon' for division is helpful for yieldings a large (but non-missing) value that will preserve participation in subsequent rankings

        # curr_liab must be non-negative here (probably not necessary)
        curr_liab.conditional_nullify_inplace(curr_liab < 0)

        ebitda2curr_liab = ebitda_sum1y / curr_liab
        return (
            self.calendarize(ebitda2curr_liab, freq=freq, add_frame=False)
            if freq is not None
            else ebitda2curr_liab
        )

    @RootLib.temp_frame()
    def FIXEDASSETS2DEBT(self, field, **kwds_args):
        """FIXEDASSETS2DEBT = (Fixed Assets / Long Term Debt)
        Prior: HIGH LEVEL = BULLISH (Low Debt Burden for the Fixed Assets)
        """
        # DL:FIXEDASSETS2DEBT_FQ = (PPE_NET_FQ / LTD_FQ)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ppe_net = self.get_fiscal_field(
            field_prefix="PPE_NET",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        ltd = self.get_fiscal_field(
            field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control(
            "ignore_mult", "right_epsilon"
        )  # <-- Will treat missing values in right of mult/div operator as epsilon (but requires left component to be non-missing)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        # Use of 'right_epsilon' for division is helpful for yieldings a large (but non-missing) value that will preserve participation in subsequent rankings

        # ltd must be non-negative here (probably not necessary)
        ltd.conditional_nullify_inplace(ltd < 0)

        fixed_assets2debt = ppe_net / ltd
        return (
            self.calendarize(fixed_assets2debt, freq=freq, add_frame=False)
            if freq is not None
            else fixed_assets2debt
        )

    @RootLib.temp_frame()
    def DIST_TO_DEFAULT(self, field, **kwds_args):
        """
        Approximation to Merton's 'Distance to Default' Formula
        (see 'Merton For Dummies', by Hans Bystrom)
        Distance To Default = (ln(Debt/Assets) / ((Debt/Assets) - 1) / (Equity Price Volatility))
        Prior: HIGH LEVEL = BULLISH (Large Distance to Default)
        """
        # FL:DIST_TO_DEFAULT = LOG(DEBT2A) / (1 - DEBT2A) / VOLATILITY(1YR)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        ltd = self.get_fiscal_field(
            field_prefix="LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_ltd = self.get_fiscal_field(
            field_prefix="CURR_LTD",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_add", True)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        debt = ltd + curr_ltd

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)

        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- require non-missing mv but missing debt OK
        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Will treat missing values in left of mult/div operator as zero (but requires right component to be non-missing)
        lev_ratio = debt / (mv + debt)

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("ignore_mult", False)
        lev_term = lev_ratio.log() / (lev_ratio - 1.0)

        rvol_3m = self.get_calendarized_field(
            field_prefix="RVOL3M", freq=freq, lib=self
        )
        dist_to_default = lev_term / rvol_3m
        return dist_to_default

    @RootLib.temp_frame()
    def ALTMAN_Z(self, field, **kwds_args):
        """
        Altman's Z Score = measure of company health and solvency (higher = more solvent)

                     3.0 <= ALTMAN_Z < INF: Safe Company
                     1.8 <= ALTMAN_Z < 3.0: Moderate Health
                     -INF < ALTMAN_Z < 1.8: Distressed Company

        Prior: HIGH LEVEL = BULLISH ("Safe" Company)

        version = 'v1': (1968)
        ------------------------
        ALTMAN_Z = (1.2 * (WORKING_CAPITAL/ASSETS))
                 + (1.4 * (RETEARN / ASSETS))
                 + (3.3 * (EBIT / ASSETS))
                 + (0.6 * (MKTCAP / LIAB))
                 + (1.0 * (SALES / ASSETS)

        version = 'v2': (Five Factor, 1983)
        -----------------------------------
        ALTMAN_Z = (0.717 * (WORKING_CAPITAL/ASSETS))
                 + (0.847 * (RETEARN / ASSETS))
                 + (3.107 * (EBIT / ASSETS))
                 + (0.420 * (EQUITY / LIAB))
                 + (0.998 * (SALES / ASSETS)

        version = 'v3': (Four Factor 1983)
        -----------------------------------
        ALTMAN_Z = 3.25
                 + (6.56 * (WORKING_CAPITAL/ASSETS))
                 + (3.26 * (RETEARN / ASSETS))
                 + (6.72 * (EBIT / ASSETS))
                 + (1.05 * (EQUITY / LIAB))

        See: 'Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy'. (Altman, Journal of Finance, 1968)
        See: 'Predicting Financial Distress of Companies' (Altman, 2000)
        """
        # FL:ALTMAN_Z = (1.2 * (WORKING_CAPITAL/ASSETS))
        #              + (1.4 * (RETEARN / ASSETS))
        #              + (3.3 * (EBIT / ASSETS))
        #              + (0.6 * (MKTCAP / LIAB))
        #              + (1.0 * (SALES / ASSETS)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        version = self.get_property(
            "version",
            field,
            grace=True,
            resolve_templates=True,
            default_property_value="v1",
        )

        wc = self.get_fiscal_field(
            field_prefix="WC",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )

        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        liab = self.get_fiscal_field(
            field_prefix="LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        ebit_sum1y = self.get_fiscal_field(
            field_prefix="EBIT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        retearn_sum1y = self.get_fiscal_field(
            field_prefix="RETEARN",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        if version in ("v2", "v3"):
            equity = self.get_fiscal_field(
                field_prefix="EQUITY",
                fiscal_mode=fiscal_mode,
                lib=cft_lib,
                aggr_op1y=None,
                freq=None,
            )
        else:
            mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)

        RootLib().set_control(
            "ignore_add", False
        )  # <-- requires all components of the model to be non-missing
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # -----------------------------------------
        # version: 'v2'
        # [Five Factor Model Re-estimated in 1983]
        # -----------------------------------------
        if version == "v2":
            X1 = 0.717 * (wc / assets)  # <-- fiscal time/space
            X2 = 0.847 * (retearn_sum1y / assets)  # <-- fiscal time/space
            X3 = 3.107 * (ebit_sum1y / assets)  # <-- fiscal time/space
            X4 = 0.420 * (equity / liab)  # <-- fiscal time/space
            X5 = 0.998 * (sales_sum1y / assets)  # <-- fiscal time/space

            altman_z = self.calendarize(X1 + X2 + X3 + X4 + X5, freq=freq)

        # -----------------------------------------
        # version: 'v3'
        # [Four Factor Model Re-estimated in 1983]
        # [Excludes Asset Turnover Term]
        # -----------------------------------------
        elif version == "v3":
            X1 = 6.56 * (wc / assets)  # <-- fiscal time/space
            X2 = 3.26 * (retearn_sum1y / assets)  # <-- fiscal time/space
            X3 = 6.72 * (ebit_sum1y / assets)  # <-- fiscal time/space
            X4 = 1.05 * (equity / liab)  # <-- fiscal time/space

            altman_z = self.calendarize(3.25 + X1 + X2 + X3 + X4, freq=freq)

        # ----------------------------------------
        # version: 'v1'
        # [Original Five Factor Model from 1968]
        # ----------------------------------------
        else:  # elif version == 'v1': # (1968)
            X1 = 1.2 * (wc / assets)  # <-- fiscal time/space
            X2 = 1.4 * (retearn_sum1y / assets)  # <-- fiscal time/space
            X3 = 3.3 * (ebit_sum1y / assets)  # <-- fiscal time/space
            X4 = 0.6 * (mv / liab)  # <-- calendar time/space
            X5 = sales_sum1y / assets  # <-- fiscal time/space

            altman_z = (
                self.calendarize(X1 + X2 + X3 + X5, freq=freq) + X4
            )  # <-- What about ignore_add setting here??

        # Return the result
        return altman_z

    @RootLib.temp_frame()
    def TAFFLER_Z(self, field, **kwds_args):
        """
        Taffler provides a variation on Altman's Z Score
        The Taffler Z-Score measure of company health and solvency (higher = more solvent)
        Prior: HIGH LEVEL = BULLISH ("Safe" Company)

            TAFFLER_Z > 0: Company Is Solvent (Very Unlikely to Fail)
            TAFFLER_Z < 0: Company 'At Risk' (Financial Profile Similar to Previously Failed Businesses)

            TAFFLER_Z = 3.2
                    + 12.18 * (PRETAX_PROFIT / CURR_LIAB)
                    +   2.5 * (CURR_ASSETS / TOTAL_LIAB)
                    - 10.68 * (CURR_LIAB / TOTAL_ASSETS)
                    + 0.029 * ((QUICK_ASSETS - CURR_LIAB) / DAILY_OP_EXPS)

        See: 'Emprical models for the monitoring of OK corporations' (Taffler, 1983)
        See: 'Twenty-five years of the Taffler z-score model: Does it really have predictive ability?' (Agarwal & Taffler, 2007)
        """
        # FL:TAFFLER_Z =   3.2
        #              + 12.18 * (PRETAX_PROFIT / CURR_LIAB)
        #              +   2.5 * (CURR_ASSETS / TOTAL_LIAB)
        #              - 10.68 * (CURR_LIAB / TOTAL_ASSETS)
        #              + 0.029 * ((QUICK_ASSETS - CURR_LIAB) / DAILY_OP_EXPS)
        #
        #  WHERE: DAILY_OP_EXPS = ((ANNUAL SALES) - (ANNUAL PRETAX_PROFIT) - (ANNUAL DEPR)) / 365.

        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        pretaxinc_sum1y = self.get_fiscal_field(
            field_prefix="PRETAXINC",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        da_sum1y = self.get_fiscal_field(
            field_prefix="DA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        curr_liab = self.get_fiscal_field(
            field_prefix="CURR_LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_assets = self.get_fiscal_field(
            field_prefix="CURR_ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        inv = self.get_fiscal_field(
            field_prefix="INVENTORY",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        total_liab = self.get_fiscal_field(
            field_prefix="LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        total_assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        # Compute daily_op_exps
        RootLib().set_control(
            "ignore_add", False
        )  # <-- require both sales_sum1y & pretaxinc_sum1y to be non-missing
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        annual_op_exp_with_da = sales_sum1y - pretaxinc_sum1y
        RootLib().set_control(
            "ignore_add", "right"
        )  # <-- OK if da_sum1y is missing below
        daily_op_exp = (annual_op_exp_with_da - da_sum1y) / 365.0

        # Compute quick_assets
        RootLib().set_control("ignore_add", "right")  # <-- OK if inv is missing below
        quick_assets = curr_assets - inv

        # Compute ratios
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("ignore_mult", False)
        pretaxinc2curr_liab = pretaxinc_sum1y / curr_liab
        curr_assets2total_liab = curr_assets / total_liab

        RootLib().set_control(
            "ignore_mult", "left0"
        )  # <-- Treat missing curr_liab as zero in expression below
        curr_liab2total_assets = curr_liab / total_assets

        RootLib().set_control("ignore_mult", False)
        quick_assets2daily_op_exp = quick_assets / daily_op_exp

        # Compute taffler_z (is in fiscal time/space)
        taffler_z = (
            3.2
            + 12.18 * pretaxinc2curr_liab
            + 2.5 * curr_assets2total_liab
            - 10.68 * curr_liab2total_assets
            + 0.029 * quick_assets2daily_op_exp
        )

        return (
            self.calendarize(taffler_z, freq=freq, add_frame=False)
            if freq is not None
            else taffler_z
        )

    @RootLib.temp_frame()
    def OHLSON_DEFAULT(self, field, **kwds_args):
        """
        Ohlson's Default (O-Score): Gauges probability of default (higher = more likely to default)
        Prior: HIGH LEVEL = BEARISH (more likely to default)

        OHLSON_DEFAULT_FQ = -1.32
                    - 0.407 * LOG(ASSETS_)
                    + 6.03  * L2A_FQ
                    - 1.43  * WC2A_FQ
                    + 0.757 * (CURR_LIAB / CURR_ASSETS)
                    - 2.37  * (NI_SUM4Q / ASSETS)
                    - 1.83  * (EBIT_SUM4Q / LIABS)
                    + 0.285 * ((NI_SUM4Q > 0) & (NI_SUM4Q_LAG4Q > 0))
                    - 1.72  * (LIAB > ASSETS)
                    - 0.521 * ((NI_SUM4Q - NI_SUM4Q_LAG4Q) / (ABS(NI_FQ) + ABS(NI_SUM4Q_LAG4Q)))

        See Ohlson: 'Financial ratios and the probabilistic prediction of bankruptcy' (Journal of Accounting Research, 1980)
        """
        # DL:OHLSON_DEFAULT_FQ = -1.32
        #              - 0.407 * LOG(ASSETS_FQ)
        #              + 6.03  * L2A_FQ
        #              - 1.43  * WC2A_FQ
        #              + 0.757 * (CURR_LIAB_FQ / CURR_ASSETS_FQ)
        #              - 2.37  * (NI_SUM4Q_FQ / ASSETS_FQ)
        #              - 1.83  * (EBIT_SUM4Q_FQ / LIABS_FQ)
        #              + 0.285 * ((NI_SUM4Q_FQ > 0) & (NI_SUM4Q_LAG4Q_FQ > 0))
        #              - 1.72  * (LIAB_FQ > ASSETS_FQ)
        #              - 0.521 * ((NI_FQ - NI_LAG1Q_FQ) / (ABS(NI_FQ) + ABS(NI_LAG1Q_FQ)))
        #
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        wc = self.get_fiscal_field(
            field_prefix="WC",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )

        l2a = self.get_fiscal_field(
            field_prefix="L2A",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        wc2a = self.get_fiscal_field(
            field_prefix="WC2A",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        curr_liab = self.get_fiscal_field(
            field_prefix="CURR_LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        curr_assets = self.get_fiscal_field(
            field_prefix="CURR_ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        liab = self.get_fiscal_field(
            field_prefix="LIAB",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        ni_sum1y = self.get_fiscal_field(
            field_prefix="NI",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        ni_sum1y_lag1y = ni_sum1y.shift1d(fiscal_ppy, keyspace=fiscal_keyspace)

        ebit_sum1y = self.get_fiscal_field(
            field_prefix="EBIT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_compare", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        log_assets = assets.log()

        cl2ca = curr_liab / curr_assets
        ni2a = ni_sum1y / assets
        ebit2debt = ebit_sum1y / liab

        inttwo = ((ni_sum1y > 0.0) & (ni_sum1y_lag1y > 0.0)).change_dtype("float")
        oeneg = (liab > assets).change_dtype("float")
        chin = (ni_sum1y - ni_sum1y_lag1y) / (
            ni_sum1y.absolute() + ni_sum1y_lag1y.absolute()
        )

        # oscore is in fiscal time/space
        oscore = (
            -1.32
            - 0.407 * log_assets
            + 6.03 * l2a
            - 1.43 * wc2a
            + 0.757 * cl2ca
            - 2.37 * ni2a
            - 1.83 * ebit2debt
            + 0.285 * inttwo
            - 1.72 * oeneg
            - 0.521 * chin
        )

        return (
            self.calendarize(oscore, freq=freq, add_frame=False)
            if freq is not None
            else oscore
        )

    @RootLib.temp_frame()
    def CHS_DISTRESS(self, field, **kwds_args):
        """CHS_DISTRESS: Distress Score
        See Campbell, Hilscher & Szilagyi, 2005
        Prior: HIGH LEVEL = BEARISH (High Distress; Likely Failure)

        version = 'v1':
        ---------------
        chs_distress = (-9.164 - 20.264*roaa + 1.416*l2a - 7.129*excess_rets_mav \
                         + 1.411*rvol_3m - 0.045*mv_log_ratio - 2.13*cash2mvta + (0.075/b2p) - 0.058*close_nsa_log)

         version = 'v2':
        ---------------
        chs_distress = (-9.164 - 20.264*roaa + 1.416*l2mvta - 7.129*excess_rets_mav \
                         + 1.411*rvol_3m - 0.045*mv_log_ratio - 2.13*cash2mvta + (0.075/b2p) - 0.058*close_nsa_log)
        """

        # FL:CHS_DISTRESS = (-9.164 - 20.264*ROAA + 1.416*L2MVTA - 7.129*EX_RET_MAVE + 1.411*RVOL3M - 0.045*MV_LOG_RATIO - 2.13*CASH2MVTA + (0.075/B2P) - 0.058*CLOSE_LOG)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        version = self.get_property(
            "version",
            field,
            grace=True,
            resolve_templates=True,
            default_property_value="v1",
        )
        if freq is not None:
            RootLib().set_control("freq", freq)

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)

        roaa = self.get_calendarized_field(field_prefix="ROAA", freq=freq, lib=self)

        cash2mvta = self.get_calendarized_field(
            field_prefix="CASH2MVTA", freq=freq, lib=self
        )
        b2p = self.get_calendarized_field(field_prefix="B2P", freq=freq, lib=self)

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        close_nsa = self.get_calendarized_field(
            field_prefix="CLOSE_NSA",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        # l2aa = self.get_calendarized_field(field_prefix='L2AA', freq=freq, lib=self) # <-- Mentioned in CHS (2005) paper, but not actually used in 'best' CHS model
        if version == "v2":
            l2a = self.get_calendarized_field(field_prefix="L2A", freq=freq, lib=self)
        else:  # if version == 'v1':
            l2mvta = self.get_calendarized_field(
                field_prefix="L2MVTA", freq=freq, lib=self
            )

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Determine excess monthly returns
        # [Note: Compute in a monthly context,
        #        then cast to target freq]
        # --------------------------------------
        if close is None:
            raise Exception("close is None")
        elif close.is_empty:
            return Quble()
        elif isinstance(close, Quble) and close.is_undefined:
            return close.copy()
        elif dates_keyspace not in close.keyspaces:
            raise Exception(f"close.keyspaces does not contain {dates_keyspace}")

        monthly_ret_plus1 = close.asfreq("CEOM", keyspace=dates_keyspace).mratio1d(
            periods=1, keyspace=dates_keyspace
        )

        index_price_field = self.get_property(
            "index_price_field", field, grace=False, resolve_templates=True
        )
        index_price = RootLib()[index_price_field]
        if index_price is None:
            raise Exception(f"Could not procure market_index:{index_price_field}")
        elif index_price.is_empty:
            raise Exception(f"Empty market_index:{index_price_field}")
        elif dates_keyspace not in index_price.keyspaces:
            raise Exception(f"index_price.keyspaces does not contain {dates_keyspace}")

        # Massage index_price to align (freq & dates) with close
        index_price = index_price.fill1d(
            keyspace=dates_keyspace, tfill_method="pad", tfill_max=5
        ).reindex1d(index=close, keyspace=dates_keyspace)

        index_monthly_ret_plus1 = index_price.asfreq(
            freq="CEOM", keyspace=dates_keyspace
        ).mratio1d(
            periods=1, keyspace=dates_keyspace
        )  # <-- NEED TO FORCE FILL TO END OF CURRENT MONTHWITH LAST VALUE??
        index_monthly_ret_plus1 = index_monthly_ret_plus1.reindex1d(
            index=monthly_ret_plus1, keyspace=dates_keyspace
        )

        excess_rets_monthly = monthly_ret_plus1.log() - index_monthly_ret_plus1.log()
        # Note: In the CSH paper, a moving exponential weighted average of monthly excess returns is used.

        excess_rets_mav_monthly = excess_rets_monthly.mmean1d(
            18, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        excess_rets_mav = excess_rets_mav_monthly.reindex1d(
            close, keyspace=dates_keyspace, tfill_max=25
        )  # <-- resample...Need to fill to last date in original (weekday) freq here??

        # Determine mv_log_ratio
        # -------------------------
        index_mktval_field = self.get_property(
            "index_mktval_field", field, grace=False, resolve_templates=True
        )
        index_mv = RootLib()[index_mktval_field]
        if index_mv is None:
            raise Exception(
                f"Could not procure index_mktval_field:{index_mktval_field}"
            )
        index_mv = index_mv.fill1d(
            dates_keyspace, tfill_method="pad", tfill_max=5
        ).reindex1d(mv, dates_keyspace)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        mv_log_ratio = (mv / index_mv).log()

        # Determine close_nsa_log
        # ------------------------
        # Ideally want to unsplit adjust the closing price before we apply to model
        close_nsa_log = close_nsa.truncate(
            max_value=15.0
        ).log()  # <-- Using close_nsa (split-adjusted close). Also, truncated at $15/share per CHS paper
        # Compute 3mo trailing realized volatility...
        # Assume 65 business days each quarter, but only 252 non-missing (non-holiday) trading days each year
        rvol_3m = self.get_calendarized_field(
            field_prefix="RVOL3M", freq=freq, lib=self
        )

        if version == "v2":
            chs_distress = (
                -9.164
                - 20.264 * roaa
                + 1.416 * l2a
                - 7.129 * excess_rets_mav
                + 1.411 * rvol_3m
                - 0.045 * mv_log_ratio
                - 2.13 * cash2mvta
                + (0.075 / b2p)
                - 0.058 * close_nsa_log
            )
        else:  # if version == 'v1':
            chs_distress = (
                -9.164
                - 20.264 * roaa
                + 1.416 * l2mvta
                - 7.129 * excess_rets_mav
                + 1.411 * rvol_3m
                - 0.045 * mv_log_ratio
                - 2.13 * cash2mvta
                + (0.075 / b2p)
                - 0.058 * close_nsa_log
            )

        return chs_distress

    @RootLib.temp_frame()
    def BASIC_DEF_INTVL(self, field, **kwds_args):
        """BASIC_DEF_INTVL (BASIC DEFENSE INTERVAL): Measures the number of days a company could survive without revenues
        BASIC_DEF_INTVL = 365*(CASH_FQ + RECEIVABLES_FQ) / MSUM(SGA_FQ + RND_FQ + DA_FQ + TOTNETOPINTEXP_FQ + TAXES_FQ,4)
        Prior: HIGH LEVEL = BULLISH (Highly Liquid & Safe)"""
        # DL:BASIC_DEF_INTVL_FQ = 365*(CASH_FQ + RECEIVABLS_FQ) / MSUM(SGA_FQ + RND_FQ + DA_FQ + TOTNETOPINTEXP_FQ + TAXES_FQ,4)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        sga_sum1y = self.get_fiscal_field(
            field_prefix="SGA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        rnd_sum1y = self.get_fiscal_field(
            field_prefix="RND",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        da_sum1y = self.get_fiscal_field(
            field_prefix="DA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        opintexp_sum1y = self.get_fiscal_field(
            field_prefix="TOTNETOPINTEXP",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        taxes_sum1y = self.get_fiscal_field(
            field_prefix="TAXES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        RootLib().set_control("ignore_add", True)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        exp_sum1y = sga_sum1y + rnd_sum1y + da_sum1y + opintexp_sum1y + taxes_sum1y

        cash = self.get_fiscal_field(
            field_prefix="CASH",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        recvs = self.get_fiscal_field(
            field_prefix="RECEIVABLES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )

        RootLib().set_control("ignore_mult", False)
        basic_def_intvl = 365.0 * ((cash + recvs) / exp_sum1y)

        # basic_def_intvl is in fiscal time/space
        return (
            self.calendarize(basic_def_intvl, freq=freq, add_frame=False)
            if freq is not None
            else basic_def_intvl
        )

    @RootLib.temp_frame()
    def PIOTROSKI_F(self, field, **kwds_args):
        """
        Piotroski's F-Score: measure of company profitability, accounting changes & overall health (higher = healthier)
        NOTE: Ideally Piotrioski's F-Score is designed to be applied only to value stocks (high book/price)
        Prior: HIGH LEVEL = BULLISH (BETTER INVESTMENTS / HEALTHIER)

        PIOTROSKI_F_FQ:
            = (ROA > 0)
            + (ROA_DIFF4Q > 0)
            + (CFOPS > 0)
            + ((CFOPS - NIB4X) > 0)
            + (LTD2A_PCHG4Q  < 0)
            + (CURR_RATIO_DIFF4Q  < 0)
            + (SHARES_PCHG4Q  <= 0)
            + (MARGIN_GP_DIFF4Q  > 0)
            + (ASSET_TURNOVER_DIFF4Q  > 0)

        See: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers" by Piotroski (2002)
        """
        # DL:PIOTROSKI_F_FQ:
        #              = (ROA > 0)
        #              + (ROA_DIFF4Q > 0)
        #              + (CFOPS > 0)
        #              + ((CFOPS-NIB4X) > 0)
        #              + (LTD2A_PCHG4Q  < 0)
        #              + (CURR_RATIO_DIFF4Q  < 0)
        #              + (SHARES_PCHG4Q  <= 0)
        #              + (MARGIN_GP_DIFF4Q  > 0)
        #              + (ASSET_TURNOVER_DIFF4Q  > 0)
        #
        # NOTE: (CFOPS-NIB4X) = (-1*OP_ACCR_CF)  or  (CFOPS-NIB4X)/AVE4Q(ASSETS) = (-1*OP_ACCR2A_CF)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        RootLib().set_control("ignore_add", False)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_compare", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Note: preface each term with 1.0* expression to force dtype conversion or each term to float

        roa = self.get_fiscal_field(
            field_prefix="ROA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        roa_score = (roa > 0.0).change_dtype("float")
        has_roa = roa.where_not_missing()

        roa_diff1y = self.get_fiscal_field(
            field_prefix="ROA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=None,
        )
        roa_diff1y_score = (roa_diff1y > 0.0).change_dtype("float")
        has_roa_diff1y = roa_diff1y.where_not_missing()

        cfops_sum1y = self.get_fiscal_field(
            field_prefix="CFOPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        cfops_sum1y_score = (cfops_sum1y > 0.0).change_dtype("float")
        has_cfops_sum1y = cfops_sum1y.where_not_missing()

        nib4x_sum1y = self.get_fiscal_field(
            field_prefix="NI_CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        accrual_score = (cfops_sum1y > nib4x_sum1y).change_dtype("float")
        has_nib4x_sum1y = nib4x_sum1y.where_not_missing()

        ltd2a_diff1y = self.get_fiscal_field(
            field_prefix="LTD2A",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=None,
        )
        ltd2a_diff1y_score = (ltd2a_diff1y < 0.0).change_dtype("float")
        has_ltd2a_diff1y = ltd2a_diff1y.where_not_missing()

        curr_ratio_diff1y = self.get_fiscal_field(
            field_prefix="CURR_RATIO",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=None,
        )
        curr_ratio_diff1y_score = (curr_ratio_diff1y > 0.0).change_dtype("float")
        has_curr_ratio_diff1y = curr_ratio_diff1y.where_not_missing()

        shares_pchg1y = self.get_fiscal_field(
            field_prefix="SHARES_PCHG1Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        shares_pchg1y_score = (shares_pchg1y <= 0.0).change_dtype("float")
        has_shares_pchg1y = shares_pchg1y.where_not_missing()

        margin_gp_diff1y = self.get_fiscal_field(
            field_prefix="MARGIN_GP",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=None,
        )
        margin_gp_diff1y_score = (margin_gp_diff1y > 0.0).change_dtype("float")
        has_margin_gp_diff1y = margin_gp_diff1y.where_not_missing()

        asset_turnover_diff1y = self.get_fiscal_field(
            field_prefix="ASSET_TURNOVER",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="mdiff",
            freq=None,
        )
        asset_turnover_diff1y_score = (asset_turnover_diff1y > 0.0).change_dtype(
            "float"
        )
        has_asset_turnover_diff1y = asset_turnover_diff1y.where_not_missing()

        RootLib().set_control("ignore_add", True)  # <-- Possibly Dangerous (?)
        piotroski_fscore = (
            roa_score
            + roa_diff1y_score
            + cfops_sum1y_score
            + accrual_score
            + ltd2a_diff1y_score
            + curr_ratio_diff1y_score
            + shares_pchg1y_score
            + margin_gp_diff1y_score
            + asset_turnover_diff1y_score
        )

        piotroski_count = (
            has_roa.change_dtype("float")
            + has_roa_diff1y.change_dtype("float")
            + has_cfops_sum1y.change_dtype("float")
            + has_nib4x_sum1y.change_dtype("float")
            + has_ltd2a_diff1y.change_dtype("float")
            + has_curr_ratio_diff1y.change_dtype("float")
            + has_shares_pchg1y.change_dtype("float")
            + has_margin_gp_diff1y.change_dtype("float")
            + has_asset_turnover_diff1y.change_dtype("float")
        )

        # Require atleast five of the metrics to be present for a non-missing fscore
        piotroski_fscore.conditional_nullify_inplace(piotroski_count < 5)

        # piotroski_fscore is in fiscal time/space
        return (
            self.calendarize(piotroski_fscore, freq=freq, add_frame=False)
            if freq is not None
            else piotroski_fscore
        )

    # ======================================= SECURITY RISK FACTORS ===========================================

    def get_rvol_daily(
        self, field, bdays, diff_bdays=None, apply_freq=True, **kwds_args
    ):
        """get_rvol_daily: RETURNS REALIZED PRICE VOLATILITY OVER SPECIFIED TRAILING # BUSINESS DAYS"""
        # Compute trailing realized price volatility...
        # Assume 261 business days each year, but only 252 non-missing (non-holiday) trading days each year
        prc_lib = self.get_property("prc_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        daily_returns = self.get_calendarized_field(
            field_prefix="TRET", freq="WEEKDAY", lib=prc_lib
        )
        rvol_daily = daily_returns.mstd1d(
            periods=bdays,
            keyspace=dates_keyspace,
            pct_required=0.5,
            ignore_missing=True,
        ) * np.sqrt(252.0)

        if diff_bdays:
            rvol_daily = rvol_daily.mdiff1d(diff_bdays, keyspace=dates_keyspace)

        if apply_freq:
            freq = self.get_property(
                "freq", field, grace=True, resolve_templates=True
            )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
            return rvol_daily.asfreq(freq=freq, keyspace=dates_keyspace)
        else:
            return rvol_daily

    @RootLib.temp_frame()
    def RVOL1M(self, field, **kwds_args):
        return self.get_rvol_daily(field=field, bdays=22, **kwds_args)

    @RootLib.temp_frame()
    def RVOL3M(self, field, **kwds_args):
        return self.get_rvol_daily(field=field, bdays=65, **kwds_args)

    @RootLib.temp_frame()
    def RVOL6M(self, field, **kwds_args):
        return self.get_rvol_daily(field=field, bdays=130, **kwds_args)

    @RootLib.temp_frame()
    def RVOL1Y(self, field, **kwds_args):
        return self.get_rvol_daily(field=field, bdays=261, **kwds_args)

    @RootLib.temp_frame()
    def RVOL1M_DIFF1M(self, field, **kwds_args):
        # FL:RVOL1M_DIFF1M = MDIFF(RVOL3M,22D) aka SPIKE IN 1M REALIZED VOL
        # DIRECTION: VOLATILITY SPIKE: BAD (SHORT)
        return self.get_rvol_daily(field=field, bdays=22, diff_bdays=22, **kwds_args)

    @RootLib.temp_frame()
    def RVOL3M_DIFF1M(self, field, **kwds_args):
        # FL:RVOL3M_DIFF1M = MDIFF(RVOL3M,22D) aka SPIKE IN 3M REALIZED VOL
        # DIRECTION: VOLATILITY SPIKE: BAD (SHORT)
        return self.get_rvol_daily(field=field, bdays=65, diff_bdays=22, **kwds_args)

    @RootLib.temp_frame()
    def RVOL6M_DIFF1M(self, field, **kwds_args):
        # FL:RVOL6M_DIFF22D = MDIFF(RVOL1Y,22D) aka SPIKE IN 6M REALIZED VOL
        # DIRECTION: VOLATILITY SPIKE: BAD (SHORT)
        return self.get_rvol_daily(field=field, bdays=130, diff_bdays=22, **kwds_args)

    @RootLib.temp_frame()
    def RVOL1Y_DIFF1M(self, field, **kwds_args):
        # FL:RVOL1Y_DIFF22D = MDIFF(RVOL1Y,22D) aka SPIKE IN 1Y REALIZED VOL
        # DIRECTION: VOLATILITY SPIKE: BAD (SHORT)
        return self.get_rvol_daily(field=field, bdays=261, diff_bdays=22, **kwds_args)

    @RootLib.temp_frame()
    def LLTV(self, field, **kwds_args):
        # FL:LLTV = AVE(Z(RVOL1Y_LAG3M),Z(RVOL1Y_LAG6M),Z(RVOL1Y_LAG1Y)) -  Z(RVOL1Y_DIFF22D)
        # DB: LONG-LONG-TERM VOLATILITY (BEING LONG THE LONG-TERM VOLATILITY)
        # LOGIC: GO LONG STOCKS THAT HAVE HAD HIGH & STABLE REALIZED VOLATILITY IN THE PAST
        #        BUT ALSO HAVE NOT EXPERIENCED A RECENT VOLATILITY SPIKE
        # DIRECTION: STABLE LONG-TERM VOLATILITY: GOOD

        id_keyspace = self.get_property(
            "id_keyspace", field, grace=True, default_property_value="SECMSTR"
        )
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is None:
            raise Exception("Could not establish non-trivial freq property")
        else:
            RootLib().set_control("freq", freq)

        periods_per_year = datetools.ppy(freq)

        rvol1y_daily = self.get_rvol_daily(
            field=field, bdays=261, apply_freq=False, **kwds_args
        )
        rvol1y_diff22d_daily = rvol1y_daily.mdiff1d(periods=22, keyspace=dates_keyspace)

        rvol1y = rvol1y_daily.asfreq(freq=freq, keyspace=dates_keyspace)
        rvol1y_diff22d = rvol1y_diff22d_daily.asfreq(freq=freq, keyspace=dates_keyspace)

        rvol1y_lag3m = rvol1y.shift1d(
            periods=int(periods_per_year / 4.0), keyspace=dates_keyspace
        )
        rvol1y_lag6m = rvol1y.shift1d(
            periods=int(periods_per_year / 2.0), keyspace=dates_keyspace
        )
        rvol1y_lag1y = rvol1y.shift1d(
            periods=int(periods_per_year), keyspace=dates_keyspace
        )

        LTVs = rvol1y_lag3m.insert_keyspace(
            keyspace="Lags", key="3M", col_type="varchar(3)"
        )
        LTVs.merge(
            rvol1y_lag6m.insert_keyspace(
                keyspace="Lags", key="6M", col_type="varchar(3)"
            ),
            inplace=True,
        )
        LTVs.merge(
            rvol1y_lag1y.insert_keyspace(
                keyspace="Lags", key="1Y", col_type="varchar(3)"
            ),
            inplace=True,
        )

        ZLTVs = LTVs.zscore1d(
            keyspace=id_keyspace, ignore_missing=True, pct_required=0.3
        )
        MeanZLTV = ZLTVs.mean1d(
            keyspace="Lags", ignore_missing=True, pct_required=0.5, auto_squeeze=True
        )
        ZSTVSpike = rvol1y_diff22d.zscore1d(
            keyspace=id_keyspace, ignore_missing=True, pct_required=0.3
        )

        RootLib().set_control(
            "ignore_add", False
        )  # <-- Want to requite that both terms below are available and non-missing
        lltv = MeanZLTV - ZSTVSpike
        return lltv

    @RootLib.temp_frame()
    def LOG_CLOSE_NSA(self, field, **kwds_args):
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        close_nsa = self.get_calendarized_field(
            field_prefix="CLOSE_NSA", freq=freq, lib=prc_lib
        )
        return close_nsa.log()  # <-- THIS SHOULD IDEALLY BE UNSPLIT ADJUSTED

    @RootLib.temp_frame()
    def LOG_MKTCAP(self, field, **kwds_args):
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        return mv.log()

    @RootLib.temp_frame()
    def LOG_ASSETS(self, field, **kwds_args):
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        assets = self.get_fiscal_field(
            field_prefix="ASSETS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        return (
            self.calendarize(assets.log(), freq=freq, add_frame=False)
            if freq is not None
            else assets.log()
        )

    @RootLib.temp_frame()
    def SHARE_TURNOVER_1M(self, field, **kwds_args):
        """SHARE_TURNOVER_1M: SHARE TURNOVER PAST 1 MONTH = MONTHLY_VOLUME / MONTHLY_SHARES"""
        # FL:SHARE_TURNOVER_1M = MSUM(VOLUME,22BD) / SHARES
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq: {freq}")
        else:
            RootLib().set_control("freq", freq)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        monthly_volume = self.get_calendarized_field(
            field_prefix="VOLUME_NSA", freq=freq, lib=prc_lib
        )  # <-- VOLUME_NSA In Ones
        monthly_shares = 1000.0 * self.get_calendarized_field(
            field_prefix="NUM_SHARES_NSA", freq=freq, lib=prc_lib
        )  # <-- NUM_SHARES_NSA In Thousands of Shares
        share_turnover = monthly_volume / monthly_shares

        return share_turnover

    @RootLib.temp_frame()
    def SHARE_TURNOVER_4W(self, field, **kwds_args):
        """SHARE_TURNOVER_4W: SHARE TURNOVER PAST 4 WEEKS = MSUM(WEEKLY_VOLUME,4W) / MMEAN(WEEKLY_SHARES,4W)"""
        # FL:SHARE_TURNOVER_1M = MSUM(VOLUME,22BD) / SHARES
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(f"Invalid freq: {freq}")
        else:
            RootLib().set_control("freq", freq)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        weekly_volume = self.get_calendarized_field(
            field_prefix="VOLUME_NSA", freq=freq, lib=prc_lib
        )  # <-- VOLUME_NSA In Ones
        volume_msum = weekly_volume.msum1d(
            periods=4, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        weekly_shares = 1000.0 * self.get_calendarized_field(
            field_prefix="NUM_SHARES_NSA", freq=freq, lib=prc_lib
        )  # <-- NUM_SHARES_NSA In Thousands of Shares
        shares_mmean = weekly_shares.mmean1d(
            periods=4, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        share_turnover = volume_msum / shares_mmean

        return share_turnover

    @RootLib.temp_frame()
    def SHARE_TURNOVER_22D(self, field, **kwds_args):
        """SHARE_TURNOVER_1M: SHARE TURNOVER PAST 22 BDAYS = MSUM(DAILY_VOLUME,22BD) / MMEAN(DAILY_SHARES,22BD)"""
        # FL:SHARE_TURNOVER_1M = MSUM(VOLUME,22BD) / SHARES
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq: {freq}")
        else:
            RootLib().set_control("freq", freq)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        daily_volume = self.get_calendarized_field(
            field_prefix="VOLUME_NSA", freq=freq, lib=prc_lib
        )  # <-- VOLUME_NSA In Ones
        volume_msum = daily_volume.msum1d(
            periods=22, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        daily_shares = 1000.0 * self.get_calendarized_field(
            field_prefix="NUM_SHARES_NSA", freq=freq, lib=prc_lib
        )  # <-- NUM_SHARES_NSA In Thousands of Shares
        shares_mmean = daily_shares.mmean1d(
            periods=22, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        share_turnover = volume_msum / shares_mmean

        return share_turnover

    @RootLib.temp_frame()
    def SHARE_TURNOVER_6M(self, field, **kwds_args):
        """SHARE_TURNOVER_6M: SHARE TURNOVER PAST 1 MONTH = MONTHLY_VOLUME / MONTHLY_SHARES"""
        # FL:SHARE_TURNOVER_1M = MSUM(VOLUME,22BD) / SHARES
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq: {freq}")
        else:
            RootLib().set_control("freq", freq)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        monthly_volume = self.get_calendarized_field(
            field_prefix="VOLUME_NSA", freq=freq, lib=prc_lib
        )  # <-- VOLUME_NSA In Ones
        volume_msum = monthly_volume.msum1d(
            periods=6, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        monthly_shares = 1000.0 * self.get_calendarized_field(
            field_prefix="NUM_SHARES_NSA", freq=freq, lib=prc_lib
        )  # <-- NUM_SHARES_NSA In Thousands of Shares
        shares_mmean = monthly_shares.mmean1d(
            periods=6, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        share_turnover = volume_msum / shares_mmean

        return share_turnover

    @RootLib.temp_frame()
    def SHARE_TURNOVER_26W(self, field, **kwds_args):
        """SHARE_TURNOVER_26W: SHARE TURNOVER PAST 26 WEEKS = MSUM(WEEKLY_VOLUME,26W) / MMEAN(WEEKLY_SHARES,26W)"""
        # FL:SHARE_TURNOVER_1M = MSUM(VOLUME,22BD) / SHARES
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(f"Invalid freq: {freq}")
        else:
            RootLib().set_control("freq", freq)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        weekly_volume = self.get_calendarized_field(
            field_prefix="VOLUME_NSA", freq=freq, lib=prc_lib
        )  # <-- VOLUME_NSA In Ones
        volume_msum = weekly_volume.msum1d(
            periods=26, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        weekly_shares = 1000.0 * self.get_calendarized_field(
            field_prefix="NUM_SHARES_NSA", freq=freq, lib=prc_lib
        )  # <-- NUM_SHARES_NSA In Thousands of Shares
        shares_mmean = weekly_shares.mmean1d(
            periods=26, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        share_turnover = volume_msum / shares_mmean

        return share_turnover

    @RootLib.temp_frame()
    def SHARE_TURNOVER_130D(self, field, **kwds_args):
        """SHARE_TURNOVER_130D: SHARE TURNOVER PAST 130 BUSINESS DAYS = MSUM(DAILY,VOLUME,130BD) / MMEAN(DAILY_SHARES,130BD)"""
        # FL:SHARE_TURNOVER_1M = MSUM(VOLUME,22BD) / SHARES
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq: {freq}")
        else:
            RootLib().set_control("freq", freq)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        daily_volume = self.get_calendarized_field(
            field_prefix="VOLUME_NSA", freq=freq, lib=prc_lib
        )  # <-- VOLUME_NSA In Ones
        volume_msum = daily_volume.msum1d(
            periods=130, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        daily_shares = 1000.0 * self.get_calendarized_field(
            field_prefix="NUM_SHARES_NSA", freq=freq, lib=prc_lib
        )  # <-- NUM_SHARES_NSA In Thousands of Shares
        shares_mmean = daily_shares.mmean1d(
            periods=130, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        share_turnover = volume_msum / shares_mmean

        return share_turnover

    @RootLib.temp_frame()
    def DLR_VOLUME(self, field, **kwds_args):
        """DLR_VOLUME: DOLLAR VOLUME = CLOSE * SHARE VOLUME"""
        # DL:DLR_VOLUME = (CLOSE * VOLUME)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dlr_volume = None  # <-- Initialization

        # First, see if DLR_VOLUME exists in prc_lib
        if freq in AlphaLib.freq2suffix:
            prc_field = f"DLR_VOLUME{AlphaLib.freq2suffix[freq]}"
            if prc_field in RootLib()[prc_lib].fields():
                dlr_volume = self.get_calendarized_field(
                    field_prefix="DLR_VOLUME", freq=freq, lib=prc_lib
                )

        # Otherwise, build DLR_VOLUME from (close * volume)
        if dlr_volume is None:
            close = self.get_calendarized_field(
                field_prefix="CLOSE_NSA", freq=freq, lib=prc_lib
            )
            volume = self.get_calendarized_field(
                field_prefix="VOLUME_NSA", freq=freq, lib=prc_lib
            )
            dlr_volume = close * volume

        return dlr_volume

    # =================================== BUSINESS QUALITY FACTORS ===========================================

    @RootLib.temp_frame()
    def CF1YPS(self, field, **kwds_args):
        """Cash Flow Per Share = MSUM(Cash Flow,4Q) / Shares"""
        # DL:CF4QPS_FQ = MSUM(CF_FQ,4)/SHARES_FQ
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        cf_sum1y = self.get_fiscal_field(
            field_prefix="CF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        shares = self.get_fiscal_field(
            field_prefix="SHARES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = cf_sum1y / shares
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def FCF1YPS(self, field, **kwds_args):
        """Free Cash Flow Per Share = MSUM(Free Cash Flow,4Q) / Shares"""
        # DL:FCF4QPS_FQ = MSUM(FCF_FQ,4)/SHARES_FQ
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        fcf_sum1y = self.get_fiscal_field(
            field_prefix="FCF",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        shares = self.get_fiscal_field(
            field_prefix="SHARES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = fcf_sum1y / shares
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def SALES1YPS(self, field, **kwds_args):
        """Sales Per Share = MSUM(Sales,4Q) / Shares"""
        # DL:FCF4QPS_FQ = MSUM(FCF_FQ,4)/SHARES_FQ
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        shares = self.get_fiscal_field(
            field_prefix="SHARES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            freq=None,
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        result = sales_sum1y / shares
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    def _coefvar_fn(
        self, src_quble, periods, fiscal_keyspace, add_frame=False, **kwds_args
    ):
        """Generates the rolling coefficient of variation statistic for the provided Quble"""
        if periods < 2:
            raise Exception("periods>=2 expected")

        # Add a temporary frame (if instructed)
        if add_frame:
            RootLib().add_frame()

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        # DECIDED TO IMPLEMENT FORMULA REQUIRING ALL PERIODS TO HAVE NO MISSING DATA (FORMULA GETS COMPLICATED OTHERWISE)
        src_squared = src_quble * src_quble.deep_copy()
        src_meanN = src_quble.mmean1d(
            periods, keyspace=fiscal_keyspace, pct_required=1.0, ignore_missing=True
        )
        src_sumN = src_quble.msum1d(
            periods, keyspace=fiscal_keyspace, pct_required=1.0, ignore_missing=True
        )  # <-- MAY NOT BE CORRECT TO ASSUME ebitda_mean12q_q = (ebitda_sum12q_q/12.) DOE TO POSSIBLE MISSING DATA POINTS
        src_squared_sumN = src_squared.msum1d(
            periods, keyspace=fiscal_keyspace, pct_required=1.0, ignore_missing=True
        )

        numerator = (
            ((periods * src_squared_sumN) - (src_sumN * src_sumN.deep_copy()))
            / (periods * (periods - 1))
        ).sqrt()
        denominator = src_meanN.absolute()

        # Require denominator to be non-negative
        denominator.conditional_nullify_inplace(denominator < 0)

        result = numerator / denominator

        # Pop the temporary frame (if applicable)
        if add_frame:
            RootLib().pop_frame()

        return result

    def _mrsq_fn(
        self,
        src_quble,
        periods,
        id_keyspace,
        fiscal_keyspace,
        add_frame=False,
        **kwds_args,
    ):
        # Add a temporary frame (if instructed)
        if add_frame:
            RootLib().add_frame()

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        if src_quble is None:
            return src_quble
        elif not isinstance(src_quble, Quble):
            raise Exception("Quble expected")
        elif src_quble.is_undefined:
            return src_quble.copy()
        elif src_quble.is_nonvariate or src_quble.valuespace is None:
            raise Exception("Variate Quble required")
        else:
            dep_var_valuespace = src_quble.valuespace

        src_quble2 = src_quble.datetime_to_freq_idx1d(
            space="<first_time_keyspace>",
            freq_idx_space="freq_idx",
            as_new_valuespace_flag=True,
        )
        offset_key = "CONSTANT_TERM"
        yxkeys = src_quble2.valuespaces + [offset_key]

        (
            ols_detail,
            ols_summary,
            fitted_values,
            resid_values,
        ) = src_quble2.mestimate_ols(
            periods=periods,
            yxkeys=yxkeys,
            sample_keyspace=fiscal_keyspace,
            offset_key=offset_key,
            pct_required=0.5,
            ignore_missing=True,
            ols_method=None,
            summary_keyspace="OLS_SUMMARY",
        )

        result = ols_summary.get("OLS_SUMMARY:RSQ", auto_squeeze=True)

        # Pop the temporary frame (if applicable)
        if add_frame:
            RootLib().pop_frame()

        return result

    @RootLib.temp_frame()
    def EPS_COEFVAR3Y(self, field, **kwds_args):
        """EPS_COEFVAR3Y: COEFFICIENT OF VARIATION OF SUM(EPS_FQ,4) OVER THE PAST 3 YEARS (12 QUARTERS)
        EPS_COEFVAR3Y_FQ = SQRT[(12.*MSUM(EPS_SUM4Q_FQ**2,12) - MSUM(EPS_SUM4Q_FQ,12)**2)/(12*(12-1))] / ABS(MMEAN(EPS_SUM4Q_FQ,12))
        WHERE: EPS_SUM4Q_FQ = SUM(EPS_FQ,4)
        """
        # DL:EPS_COEFVAR3Y_FQ = SQRT[(12*MSUM(EPS_SUM4Q_FQ**2,12) - MSUM(EPS_SUM4Q_FQ,12)**2)/(12*(12-1))] / ABS(MMEAN(EPS_SUM4Q_FQ,12))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        eps_sum1y = self.get_fiscal_field(
            field_prefix="EPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._coefvar_fn(
            eps_sum1y,
            periods=3 * fiscal_ppy,
            fiscal_keyspace=fiscal_keyspace,
            **kwds_args,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def CFPS_COEFVAR3Y(self, field, **kwds_args):
        """CFPS_COEFVAR3Y_FQ: COEFFICIENT OF VARIATION OF CF1YPS OVER THE PAST 3 YEARS (12 QUARTERS)
        CFPS_COEFVAR3Y_FQ = SQRT[(12.*MSUM(CF1YPS**2,12) - MSUM(CF1YPS,12)**2)/(12*(12-1))] / ABS(MMEAN(CF1YPS,12))
        WHERE: CF1YPS_FQ = (SUM(CF_FQ,4)/SHARES_FQ)
        """
        # DL:CFPS_COEFVAR3Y_FQ = SQRT[(12*MSUM(CF1YPS_FQ**2,12) - MSUM(CF1YPS_FQ,12)**2)/(12*(12-1))] / ABS(MMEAN(CF1YPS_FQ,12))
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        cf_sum1y_ps = self.get_fiscal_field(
            field_prefix="CF1YPS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._coefvar_fn(
            cf_sum1y_ps,
            periods=3 * fiscal_ppy,
            fiscal_keyspace=fiscal_keyspace,
            **kwds_args,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def FCFPS_COEFVAR3Y(self, field, **kwds_args):
        """FCFPS_COEFVAR3Y_FQ: COEFFICIENT OF VARIATION OF FCF1YPS OVER THE PAST 3 YEARS (12 QUARTERS)
        FCFPS_COEFVAR3Y_FQ = SQRT[(12.*MSUM(FCF1YPS**2,12) - MSUM(FCF1YPS,12)**2)/(12*(12-1))] / ABS(MMEAN(FCF1YPS,12))
        WHERE: FCF1YPS_FQ = (SUM(FCF_FQ,4)/SHARES_FQ)
        """
        # DL:FCFPS_COEFVAR3Y_FQ = SQRT[(12*MSUM(FCF1YPS_FQ**2,12) - MSUM(FCF1YPS_FQ,12)**2)/(12*(12-1))] / ABS(MMEAN(FCF1YPS_FQ,12))
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        fcf_sum1y_ps = self.get_fiscal_field(
            field_prefix="FCF1YPS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._coefvar_fn(
            fcf_sum1y_ps,
            periods=3 * fiscal_ppy,
            fiscal_keyspace=fiscal_keyspace,
            **kwds_args,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def SPS_COEFVAR3Y(self, field, **kwds_args):
        """SPS_COEFVAR3Y_FQ: COEFFICIENT OF VARIATION OF SALES1YPS_FQ=SUM(SALES_FQ,4) OVER THE PAST 3 YEARS (12 QUARTERS)
        SPS_COEFVAR3Y_FQ = SQRT[(12.*MSUM(S4QPS**2,12) - MSUM(S4QPS,12)**2)/(12*(12-1))] / ABS(MMEAN(SALES1YPS_FQ,12))
        WHERE: SALES1YPS_FQ = (SUM(SALES_FQ,4)/SHARES_FQ)
        """
        # DL:SPS_COEFVAR3Y_FQ = SQRT[(12*MSUM(SALES1YPS_FQ**2,12) - MSUM(SALES1YPS_FQ,12)**2)/(12*(12-1))] / ABS(MMEAN(SALES1YPS_FQ,12))
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        sales_sum1y_ps = self.get_fiscal_field(
            field_prefix="SALES1YPS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._coefvar_fn(
            sales_sum1y_ps,
            periods=3 * fiscal_ppy,
            fiscal_keyspace=fiscal_keyspace,
            **kwds_args,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def EBITDA_COEFVAR3Y(self, field, **kwds_args):
        """EBITDA_COEFVAR3Y_FQ: COEFFICIENT OF VARIATION OF SUM(EBITDA_FQ,4) OVER THE PAST 3 YEARS (12 QUARTERS)
        EBITDA_COEFVAR3Y_FQ = SQRT[(12.*MSUM(EBITDA_SUM4Q_FQ**2,12) - MSUM(EBITDA_SUM4Q_FQ,12)**2)/(12*(12-1))] / ABS(MMEAN(EBITDA_SUM4Q_FQ,12))
        WHERE: EBITDA_SUM4Q_FQ = SUM(EBITDA_FQ,4)
        """
        # DL:EBITDA_COEFVAR3Y_FQ = SQRT[(12*MSUM(EBITDA_SUM4Q_FQ**2,12) - MSUM(EBITDA_SUM4Q_FQ,12)**2)/(12*(12-1))] / ABS(MMEAN(EBITDA_SUM4Q_FQ,12))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        ebitda_sum1y = self.get_fiscal_field(
            field_prefix="EBITDA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._coefvar_fn(
            ebitda_sum1y,
            periods=3 * fiscal_ppy,
            fiscal_keyspace=fiscal_keyspace,
            **kwds_args,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def EPS_COEFVAR5Y(self, field, **kwds_args):
        """EPS_COEFVAR5Y: COEFFICIENT OF VARIATION OF SUM(EPS_FQ,4) OVER THE PAST 5 YEARS (20 QUARTERS)
        EPS_COEFVAR5Y_FQ = SQRT[(20.*MSUM(EPS_SUM4Q_FQ**2,20) - MSUM(EPS_SUM4Q_FQ,20)**2)/(20*(20-1))] / ABS(MMEAN(EPS_SUM4Q_FQ,20))
        WHERE: EPS_SUM4Q_FQ = SUM(EPS_FQ,4)
        """
        # DL:EPS_COEFVAR5Y_FQ = SQRT[(20*MSUM(EPS_SUM4Q_FQ**2,20) - MSUM(EPS_SUM4Q_FQ,20)**2)/(20*(20-1))] / ABS(MMEAN(EPS_SUM4Q_FQ,20))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        eps_sum1y = self.get_fiscal_field(
            field_prefix="EPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._coefvar_fn(
            eps_sum1y,
            periods=5 * fiscal_ppy,
            fiscal_keyspace=fiscal_keyspace,
            **kwds_args,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def CFPS_COEFVAR5Y(self, field, **kwds_args):
        """CFPS_COEFVAR5Y_FQ: COEFFICIENT OF VARIATION OF CF1YPS OVER THE PAST 5 YEARS (20 QUARTERS)
        CFPS_COEFVAR5Y_FQ = SQRT[(20.*MSUM(CF4QPS**2,20) - MSUM(CF4QPS,20)**2)/(20*(20-1))] / ABS(MMEAN(CF1YPS,20))
        WHERE: CF1YPS_FQ = (SUM(CF_FQ,4)/SHARES_FQ)
        """
        # DL:CFPS_COEFVAR5Y_FQ = SQRT[(20*MSUM(CF1YPS_FQ**2,20) - MSUM(CF1YPS_FQ,20)**2)/(20*(20-1))] / ABS(MMEAN(CF1YPS_FQ,20))
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        cf_sum1y_ps = self.get_fiscal_field(
            field_prefix="CF1YPS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._coefvar_fn(
            cf_sum1y_ps,
            periods=5 * fiscal_ppy,
            fiscal_keyspace=fiscal_keyspace,
            **kwds_args,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def FCFPS_COEFVAR5Y(self, field, **kwds_args):
        """FCFPS_COEFVAR5Y_FQ: COEFFICIENT OF VARIATION OF FCF1YPS OVER THE PAST 5 YEARS (20 QUARTERS)
        FCFPS_COEFVAR5Y_FQ = SQRT[(20.*MSUM(FCF1YPS**2,20) - MSUM(FCF1YPS,20)**2)/(20*(20-1))] / ABS(MMEAN(FCF1YPS,20))
        WHERE: FCF1YPS_FQ = (SUM(FCF_FQ,4)/SHARES_FQ)
        """
        # DL:FCFPS_COEFVAR5Y_FQ = SQRT[(20*MSUM(FCF1YPS_FQ**2,20) - MSUM(FCF4QPS_FQ,20)**2)/(20*(20-1))] / ABS(MMEAN(FCF1YPS_FQ,20))
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        fcf_sum1y_ps = self.get_fiscal_field(
            field_prefix="FCF1YPS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._coefvar_fn(
            fcf_sum1y_ps,
            periods=5 * fiscal_ppy,
            fiscal_keyspace=fiscal_keyspace,
            **kwds_args,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def SPS_COEFVAR5Y(self, field, **kwds_args):
        """SPS_COEFVAR5Y_FQ: COEFFICIENT OF VARIATION OF SALES1YPS_FQ=SUM(SALES_FQ,4) OVER THE PAST 5 YEARS (20 QUARTERS)
        SPS_COEFVAR5Y_FQ = SQRT[(20.*MSUM(SALES1YPS_FQ**2,20) - MSUM(SALES1YPS_FQ,20)**2)/(20*(20-1))] / ABS(MMEAN(SALES1YPS_FQ,20))
        WHERE: SALES1YPS_FQ = (SUM(SALES_FQ,4)/SHARES_FQ)
        """
        # DL:SPS_COEFVAR5Y_FQ = SQRT[(20*MSUM(SALES1YPS_FQ**2,20) - MSUM(SALES1YPS_FQ,20)**2)/(20*(20-1))] / ABS(MMEAN(SALES1YPS_FQ,20))
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        sales_sum1y_ps = self.get_fiscal_field(
            field_prefix="SALES1YPS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._coefvar_fn(
            sales_sum1y_ps,
            periods=5 * fiscal_ppy,
            fiscal_keyspace=fiscal_keyspace,
            **kwds_args,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def EBITDA_COEFVAR5Y(self, field, **kwds_args):
        """EBITDA_COEFVAR5Y_FQ: COEFFICIENT OF VARIATION OF SUM(EBITDA_FQ,4) OVER THE PAST 5 YEARS (20 QUARTERS)
        EBITDA_COEFVAR5Y_FQ = SQRT[(20.*MSUM(EBITDA_SUM4Q_FQ**2,20) - MSUM(EBITDA_SUM4Q_FQ,20)**2)/(20*(20-1))] / ABS(MMEAN(EBITDA_SUM4Q_FQ,20))
        WHERE: EBITDA_SUM5Q_FQ = SUM(EBITDA_FQ,4)
        """
        # DL:EBITDA_COEFVAR5Y_FQ = SQRT[(20*MSUM(EBITDA_SUM4Q_FQ**2,20) - MSUM(EBITDA_SUM4Q_FQ,20)**2)/(20*(20-1))] / ABS(MMEAN(EBITDA_SUM4Q_FQ,20))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        ebitda_sum1y = self.get_fiscal_field(
            field_prefix="EBITDA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._coefvar_fn(
            ebitda_sum1y,
            periods=5 * fiscal_ppy,
            fiscal_keyspace=fiscal_keyspace,
            **kwds_args,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def EPS_TREND_RSQ5Y(self, field, **kwds_args):
        """EPS_TREND_RSQ5Y_FQ: R-SQUARED OF ROLLING 5 YEARS EPS TRENDLINE (REGRESSION PERFORMED WITH WITH OFFSET)"""
        return self._EPS_TREND_RSQNY(field, periods=5, **kwds_args)

    @RootLib.temp_frame()
    def EPS_TREND_RSQ3Y(self, field, **kwds_args):
        """EPS_TREND_RSQ3Y_FQ: R-SQUARED OF ROLLING 3 YEARS EPS TRENDLINE (REGRESSION PERFORMED WITH WITH OFFSET)"""
        return self._EPS_TREND_RSQNY(field, periods=3, **kwds_args)

    @RootLib.temp_frame()
    def _EPS_TREND_RSQNY(self, field, periods, **kwds_args):
        """EPS_TREND_RSQ_FQ: R-SQUARED OF ROLLING N YEARS EPS TRENDLINE (REGRESSION PERFORMED WITH WITH OFFSET)"""
        # DL:EPS_TREND_RSQ3Y_FQ = MSQR(MSUM(EPS_FQ,4),12)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        eps_sum1y = self.get_fiscal_field(
            field_prefix="EPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        if eps_sum1y.is_multivariate:
            eps_sum1y = eps_sum1y.to_univariate()
        id_keyspace = eps_sum1y.id_keyspace()  # <-- In case a ref_lib was provided

        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._mrsq_fn(
            eps_sum1y,
            periods=periods * fiscal_ppy,
            id_keyspace=id_keyspace,
            fiscal_keyspace=fiscal_keyspace,
            add_frame=False,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def CFPS_TREND_RSQ5Y(self, field, **kwds_args):
        """CFPS_TREND_RSQ5Y: R-SQUARED OF ROLLING 5 YEARS CF4QPS TRENDLINE (REGRESSION PERFORMED WITH WITH OFFSET)
        WHERE: CF4QPS_FQ = [SUM(CF_FQ,4)/SHARES_FQ]"""
        return self._CFPS_TREND_RSQNY(field, periods=5, **kwds_args)

    @RootLib.temp_frame()
    def CFPS_TREND_RSQ3Y(self, field, **kwds_args):
        """CFPS_TREND_RSQ3Y: R-SQUARED OF ROLLING 3 YEARS CF4QPS TRENDLINE (REGRESSION PERFORMED WITH WITH OFFSET)
        WHERE: CF4QPS_FQ = [SUM(CF_FQ,4)/SHARES_FQ]"""
        return self._CFPS_TREND_RSQNY(field, periods=3, **kwds_args)

    @RootLib.temp_frame()
    def _CFPS_TREND_RSQNY(self, field, periods, **kwds_args):
        """CFPS_TREND_RSQNY: R-SQUARED OF ROLLING N YEARS CF4QPS TRENDLINE (REGRESSION PERFORMED WITH WITH OFFSET)
        WHERE: CF4QPS_FQ = [SUM(CF_FQ,4)/SHARES_FQ]"""
        # DL:CFPS_TREND_RSQ3Y_FQ = MSQR(CF4QPS_FQ,12)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        cf1yps = self.get_fiscal_field(
            field_prefix="CF1YPS",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y="msum",
            freq=None,
        )

        if cf1yps.is_multivariate:
            cf1yps = cf1yps.to_univariate()

        id_keyspace = cf1yps.id_keyspace()  # <-- In case a ref_lib was provided

        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        result = self._mrsq_fn(
            cf1yps,
            periods=periods * fiscal_ppy,
            id_keyspace=id_keyspace,
            fiscal_keyspace=fiscal_keyspace,
            add_frame=False,
        )
        return (
            self.calendarize(result, freq=freq, add_frame=False)
            if freq is not None
            else result
        )

    @RootLib.temp_frame()
    def SALES_GR1Y_STD5Y(self, field, **kwds_args):
        """SALES_GR1Y_STD5Y_FQ: 5Y (20Q) Standard Deviation of YoY (4Q) PctChange in Trailing 4Q Sales
        SALES_GR1Y_STD5Y_FQ = MSTDDEV(SALES_GR1Y_FQ,20) = MSTDDEV(MPCTCHG(SALES_SUM4Q_FQ,4),20) = MSTDDEV(MPCTCHG(MSUM(SALES_FQ,4),4),20)
        Note: This measure utilized in Mohanran's G-Score (see Mohanran, 2004)
        """
        # DL:SALES_GR1Y_STD5Y_FQ = MSTD(SALES_GR1Y_FQ,20)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        sales_gr1y = self.get_fiscal_field(
            field_prefix="SALES_GR1Y",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        sales_gr1y_std5y = sales_gr1y.mstd1d(
            5 * fiscal_ppy,
            keyspace=fiscal_keyspace,
            pct_required=0.65,
            ignore_missing=True,
        )
        return (
            self.calendarize(sales_gr1y_std5y, freq=freq, add_frame=False)
            if freq is not None
            else sales_gr1y_std5y
        )

    @RootLib.temp_frame()
    def ROA_STD5Y(self, field, **kwds_args):
        """ROA_STD5Y_FQ: 5Y (20Q) Standard Deviation of Trailing ROE
        ROA_STD5Y_FQ = MSTDDEV(ROA_FQ,20) = MSTDDEV(MPCTCHG(ROA_FQ,4),20) = MSTDDEV(MPCTCHG(MSUM(ROA_FQ,4),4),20)
        Note: This measure utilized in Mohanran's G-Score (see Mohanran, 2004)
        Prior: Higher Level = Bearish (Perverse)
        """
        # DL:ROE_STD5Y_FQ = MSTD(ROE_FQ,20)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        roa_std5y_fiscal = self.get_fiscal_field(
            field_prefix="ROA",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y=None,
            multi_year_window=5,
            multi_year_op="mstd",
            multi_year_ignore_missing=True,
            multi_year_pct_required=0.5,
            freq=None,
        )
        return (
            self.calendarize(roa_std5y_fiscal, freq=freq, add_frame=False)
            if freq is not None
            else roa_std5y_fiscal
        )

    @RootLib.temp_frame()
    def ROA_STD5Y(self, field, **kwds_args):
        """ROA_STD5Y_FQ: 5Y (20Q) Standard Deviation of ROA
        ROA_STD5Y_FQ = MSTDDEV(ROA_FQ,20)
        Note: This measure utilized in Mohanran's G-Score (see Mohanran, 2004)
        """
        # DL:ROA_STD5Y_FQ = MSTD(ROA_FQ,20)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        fiscal_keyspace = self.get_property(
            "fiscal_keyspace", field, grace=True, default_property_value="Fiscal"
        )

        roa = self.get_fiscal_field(
            field_prefix="ROA",
            fiscal_mode=fiscal_mode,
            lib=self,
            aggr_op1y=None,
            freq=None,
        )
        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        roa_std5y = roa.mstd1d(
            5 * fiscal_ppy,
            keyspace=fiscal_keyspace,
            pct_required=0.65,
            ignore_missing=True,
        )
        return (
            self.calendarize(roa_std5y, freq=freq, add_frame=False)
            if freq is not None
            else roa_std5y
        )

    @RootLib.temp_frame()
    def OPINC_LEV(self, field, **kwds_args):
        """OPINC_LEV_FQ = Operating Leverage"""
        # FL:OPINC_LEV_FQ = [MPCTCHG(MSUM(OPINC_FQ,4),4) / MPCTCHG(MSUM(SALES_FQ,4),4)]
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        opinc_sum1y = self.get_fiscal_field(
            field_prefix="OPINC",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        sales_sum1y = self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # sales_sum1y must be non-negative here
        sales_sum1y.conditional_nullify_inplace(sales_sum1y < 0)

        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        opinv_lev = opinc_sum1y / sales_sum1y
        return (
            self.calendarize(opinv_lev, freq=freq, add_frame=False)
            if freq is not None
            else opinv_lev
        )

    @RootLib.temp_frame()
    def FIN_LEV(self, field, **kwds_args):
        """FININC_LEV_FQ = Financial Leverage"""
        # FL:FIN_LEV_FQ = (MSUM(EBIT_FQ,4) / MSUM(PRETAXINC_FQ,4))
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        ebit_sum1y = self.get_fiscal_field(
            field_prefix="EBIT",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )
        pretaxinc_sum1y = self.get_fiscal_field(
            field_prefix="PRETAXINC",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            freq=None,
        )

        # pretaxinc_sum1y must be non-negative here
        pretaxinc_sum1y.conditional_nullify_inplace(pretaxinc_sum1y < 0)

        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        fin_lev = ebit_sum1y / pretaxinc_sum1y
        return (
            self.calendarize(fin_lev, freq=freq, add_frame=False)
            if freq is not None
            else fin_lev
        )

    @RootLib.temp_frame()
    def EPS_ABSDEV3Y(self, field, **kwds_args):
        """EPS_ABSDEV3Y = 3-Year (12 Quarter) Mean Absolute Deviation of EPS (Trailing 4 Quarters)"""
        # DL:EPS_ABSDEV3Y_FQ = [MMEAN(ABS(EPS_SUM4Q_FQ - MMEAN(EPS_SUM4Q_FQ,12)),12)] / MMEAN(EPS_SUM4Q_FQ,12)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        return self.get_fiscal_field(
            field_prefix="EPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            multi_year_window=(3 * fiscal_ppy),
            multi_year_op="mabsdev",
            multi_year_pct_required=0.5,
            multi_year_ignore_missing=True,
            freq=freq,
        )

    @RootLib.temp_frame()
    def SALES_ABSDEV3Y(self, field, **kwds_args):
        """SALES_ABSDEV3Y = 3-Year (12 Quarter) Mean Absolute Deviation of Sales (Trailing 4 Quarters)"""
        # DL:SALES_ABSDEV3Y_FQ = [MMEAN(ABS(SALES_SUM4Q_FQ - MMEAN(SALES_SUM4Q_FQ,12)),12)] / MMEAN(SALES_SUM4Q_FQ,12)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        return self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            multi_year_window=(3 * fiscal_ppy),
            multi_year_op="mabsdev",
            multi_year_pct_required=0.5,
            multi_year_ignore_missing=True,
            freq=freq,
        )

    @RootLib.temp_frame()
    def EPS_ABSDEV5Y(self, field, **kwds_args):
        """EPS_ABSDEV5Y = 5-Year (20 Quarter) Mean Absolute Deviation of EPS (Trailing 4 Quarters)"""
        # DL:EPS_ABSDEV5Y_FQ = [MMEAN(ABS(EPS_SUM4Q_FQ - MMEAN(EPS_SUM4Q_FQ,20)),20)] / MMEAN(EPS_SUM4Q_FQ,20)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        return self.get_fiscal_field(
            field_prefix="EPS",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            multi_year_window=(5 * fiscal_ppy),
            multi_year_op="mabsdev",
            multi_year_pct_required=0.5,
            multi_year_ignore_missing=True,
            freq=freq,
        )

    @RootLib.temp_frame()
    def SALES_ABSDEV5Y(self, field, **kwds_args):
        """SALES_ABSDEV5Y = 5-Year (20 Quarter) Mean Absolute Deviation of Sales (Trailing 4 Quarters)"""
        # DL:SALES_ABSDEV5Y_FQ = [MMEAN(ABS(SALES_SUM4Q_FQ - MMEAN(SALES_SUM4Q_FQ,20)),20)] / MMEAN(SALES_SUM4Q_FQ,20)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        fiscal_ppy = AlphaLib.fiscal_mode2ppy[fiscal_mode]
        return self.get_fiscal_field(
            field_prefix="SALES",
            fiscal_mode=fiscal_mode,
            lib=cft_lib,
            aggr_op1y="msum",
            multi_year_window=(5 * fiscal_ppy),
            multi_year_op="mabsdev",
            multi_year_pct_required=0.5,
            multi_year_ignore_missing=True,
            freq=freq,
        )

    # =================================== SELL-SIDE SENTIMENT FACTORS =======================================

    def get_est_chg(
        self,
        window_size,
        window_op,
        metric,
        prd,
        stat,
        freq,
        lib,
        dates_keyspace,
        add_frame=False,
    ):
        # Non-fiscal period estimates (Example: PTG_MEAN)
        if prd is None or (isinstance(prd, str) and len(prd) == 0):
            est_prefix = f"{metric}_{stat}{AlphaLib.freq2suffix[freq]}"
            est = self.get_calendarized_field(
                field_prefix=est_prefix, freq=freq, lib=lib
            )
            if window_op == "diff":
                return est2.mdiff1d(periods=window_size, keyspace=dates_keyspace)
            elif window_op == "pctchg":
                return est2.mpctchg1d(periods=window_size, keyspace=dates_keyspace)
            else:
                raise Exception(f"Invalid window_op:{window_op}")

        # Fiscal period estimates (Example: EPS_FY1_MEAN)
        else:
            prd2 = prd[0:-1] + str(int(prd[-1:]) + 1)

            est1_prefix = f"{metric}_{prd}_{stat}"
            est2_prefix = f"{metric}_{prd2}_{stat}"

            prdend1_prefix = f"{metric}_{prd}_PRDEND"
            prdend2_prefix = f"{metric}_{prd2}_PRDEND"

            est1 = self.get_calendarized_field(
                field_prefix=est1_prefix, freq=freq, lib=lib
            )
            prdend1 = self.get_calendarized_field(
                field_prefix=prdend1_prefix, freq=freq, lib=lib
            )
            est1_lagged = est1.shift1d(periods=window_size, keyspace=dates_keyspace)
            prdend1_lagged = prdend1.shift1d(
                periods=window_size, keyspace=dates_keyspace
            )

            est2 = self.get_calendarized_field(
                field_prefix=est2_prefix, freq=freq, lib=lib
            )
            prdend2 = self.get_calendarized_field(
                field_prefix=prdend2_prefix, freq=freq, lib=lib
            )
            est2_lagged = est2.shift1d(periods=window_size, keyspace=dates_keyspace)
            prdend2_lagged = prdend2.shift1d(
                periods=window_size, keyspace=dates_keyspace
            )

            if add_frame:
                RootLib().add_frame()

            RootLib().set_control("ignore_add", False)
            RootLib().set_control("ignore_mult", False)
            RootLib().set_control("ignore_compare", False)
            RootLib().set_control("auto_compress", True)
            RootLib().set_control("variate_mode", "uni")

            est_diff = est1.clear()

            if window_op == "diff":
                # Fiscal Period Transition Over Trialing Window
                est_diff[prdend1 == prdend2_lagged] = est1 - est2_lagged

                # No Fiscal Period Transition Over Trialing Window
                est_diff[prdend1 == prdend1_lagged] = est1 - est1_lagged
            elif window_op == "pctchg":
                # Fiscal Period Transition Over Trialing Window (Do This Step First)
                est_diff[prdend1.where_not_missing() & prdend1 == prdend2_lagged] = (
                    est1 / est2_lagged
                ) - 1.0

                # No Fiscal Period Transition Over Trialing Window (Do This Step Last)
                est_diff[prdend1.where_not_missing() & prdend1 == prdend1_lagged] = (
                    est1 / est1_lagged
                ) - 1.0

            else:
                raise Exception(f"Invalid window_op:{window_op}")

            if add_frame:
                RootLib().pop_frame()

            return est_diff

    @RootLib.temp_frame()
    def SS_EPS_FY1_MEAN_DIFF5D2P(self, field, **kwds_args):
        """SS_EPS_FY1_MEAN_DIFF5D2P = (EPS_FY1_MEAN_DIFF5D / CLOSE)"""
        # FL:SS_EPS_FY1_MEAN_DIFF5D2P = (EPS_FY1_MEAN_DIFF5D / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        eps_fy1_mean_diff = self.get_est_chg(
            window_size=5,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return eps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_EPS_FY1_MEAN_DIFF1W2P(self, field, **kwds_args):
        """SS_EPS_FY1_MEAN_DIFF1W2P = (EPS_FY1_MEAN_DIFF1W / CLOSE)"""
        # FL:SS_EPS_FY1_MEAN_DIFF1W2P = (EPS_FY1_MEAN_DIFF1W / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        eps_fy1_mean_diff = self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return eps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_EPS_FY1_MEAN_DIFF22D2P(self, field, **kwds_args):
        """SS_EPS_FY1_MEAN_DIFF22D2P = (EPS_FY1_MEAN_DIFF22D / CLOSE)"""
        # FL:SS_EPS_FY1_MEAN_DIFF22D2P = (EPS_FY1_MEAN_DIFF22D / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        eps_fy1_mean_diff = self.get_est_chg(
            window_size=22,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return eps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_EPS_FY1_MEAN_DIFF4W2P(self, field, **kwds_args):
        """SS_EPS_FY1_MEAN_DIFF4W2P = (EPS_FY1_MEAN_DIFF4W / CLOSE)"""
        # FL:SS_EPS_FY1_MEAN_DIFF4W2P = (EPS_FY1_MEAN_DIFF4W / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        eps_fy1_mean_diff = self.get_est_chg(
            window_size=4,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return eps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_EPS_FY1_MEAN_DIFF1M2P(self, field, **kwds_args):
        """SS_EPS_FY1_MEAN_DIFF1M2P = (EPS_FY1_MEAN_DIFF1M / CLOSE)"""
        # FL:SS_EPS_FY1_MEAN_DIFF1M2P = (EPS_FY1_MEAN_DIFF1M / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        eps_fy1_mean_diff = self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return eps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_EPS_FY1_MEAN_DIFF65D2P(self, field, **kwds_args):
        """SS_EPS_FY1_MEAN_DIFF65D2P = (EPS_FY1_MEAN_DIFF65D / CLOSE)"""
        # FL:SS_EPS_FY1_MEAN_DIFF65D2P = (EPS_FY1_MEAN_DIFF65D / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        eps_fy1_mean_diff = self.get_est_chg(
            window_size=65,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return eps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_EPS_FY1_MEAN_DIFF13W2P(self, field, **kwds_args):
        """SS_EPS_FY1_MEAN_DIFF13W2P = (EPS_FY1_MEAN_DIFF13W / CLOSE)"""
        # FL:SS_EPS_FY1_MEAN_DIFF13W2P = (EPS_FY1_MEAN_DIFF13W / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        eps_fy1_mean_diff = self.get_est_chg(
            window_size=13,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return eps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_EPS_FY1_MEAN_DIFF3M2P(self, field, **kwds_args):
        """SS_EPS_FY1_MEAN_DIFF3M2P = (EPS_FY1_MEAN_DIFF3M / CLOSE)"""
        # FL:SS_EPS_FY1_MEAN_DIFF3M2P = (EPS_FY1_MEAN_DIFF3M / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        eps_fy1_mean_diff = self.get_est_chg(
            window_size=3,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return eps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_DIFF5D2MV(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_DIFF5D2MV = (SAL_FY1_MEAN_DIFF5D / MKTCAP)"""
        # FL:SS_SALES_FY1_MEAN_DIFF5D2MV = (SAL_FY1_MEAN_DIFF5D / MKTCAP)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        sales_fy1_mean_diff = self.get_est_chg(
            window_size=5,
            window_op="diff",
            metric="REV",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return sales_fy1_mean_diff / mv

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_DIFF1W2MV(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_DIFF1W2P = (SAL_FY1_MEAN_DIFF1W / CLOSE)"""
        # FL:SS_SALES_FY1_MEAN_DIFF1W2P = (SAL_FY1_MEAN_DIFF1W / CLOSE)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        sales_fy1_mean_diff = self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="REV",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return sales_fy1_mean_diff / mv

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_DIFF22D2MV(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_DIFF22D2P = (SAL_FY1_MEAN_DIFF22D / CLOSE)"""
        # FL:SS_SALES_FY1_MEAN_DIFF22D2P = (SAL_FY1_MEAN_DIFF22D / CLOSE)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        sales_fy1_mean_diff = self.get_est_chg(
            window_size=22,
            window_op="diff",
            metric="REV",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return sales_fy1_mean_diff / mv

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_DIFF4W2MV(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_DIFF4W2P = (SAL_FY1_MEAN_DIFF4W / CLOSE)"""
        # FL:SS_SALES_FY1_MEAN_DIFF4W2P = (SAL_FY1_MEAN_DIFF4W / CLOSE)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        sales_fy1_mean_diff = self.get_est_chg(
            window_size=4,
            window_op="diff",
            metric="REV",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return sales_fy1_mean_diff / mv

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_DIFF1M2MV(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_DIFF1M2P = (SAL_FY1_MEAN_DIFF1M / CLOSE)"""
        # FL:SS_SALES_FY1_MEAN_DIFF1M2P = (SAL_FY1_MEAN_DIFF1M / CLOSE)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        sales_fy1_mean_diff = self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="REV",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return sales_fy1_mean_diff / mv

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_DIFF65D2MV(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_DIFF65D2P = (SAL_FY1_MEAN_DIFF65D / CLOSE)"""
        # FL:SS_SALES_FY1_MEAN_DIFF65D2P = (SAL_FY1_MEAN_DIFF65D / CLOSE)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        sales_fy1_mean_diff = self.get_est_chg(
            window_size=65,
            window_op="diff",
            metric="REV",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return sales_fy1_mean_diff / mv

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_DIFF13W2MV(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_DIFF13W2P = (SAL_FY1_MEAN_DIFF13W / CLOSE)"""
        # FL:SS_SALES_FY1_MEAN_DIFF13W2P = (SAL_FY1_MEAN_DIFF13W / CLOSE)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        sales_fy1_mean_diff = self.get_est_chg(
            window_size=13,
            window_op="diff",
            metric="REV",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return sales_fy1_mean_diff / mv

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_DIFF3M2MV(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_DIFF3M2P = (SAL_FY1_MEAN_DIFF3M / CLOSE)"""
        # FL:SS_SALES_FY1_MEAN_DIFF3M2P = (SAL_FY1_MEAN_DIFF3M / CLOSE)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        sales_fy1_mean_diff = self.get_est_chg(
            window_size=3,
            window_op="diff",
            metric="REV",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return sales_fy1_mean_diff / mv

    @RootLib.temp_frame()
    def SS_CFPS_FY1_MEAN_DIFF5D2P(self, field, **kwds_args):
        """SS_CFPS_FY1_MEAN_DIFF5D2P = (CPS_FY1_MEAN_DIFF5D / CLOSE)"""
        # FL:SS_CFPS_FY1_MEAN_DIFF5D2P = (CPS_FY1_MEAN_DIFF5D / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        cfps_fy1_mean_diff = self.get_est_chg(
            window_size=5,
            window_op="diff",
            metric="CFPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return cfps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_CFPS_FY1_MEAN_DIFF1W2P(self, field, **kwds_args):
        """SS_CFPS_FY1_MEAN_DIFF1W2P = (CPS_FY1_MEAN_DIFF1W / CLOSE)"""
        # FL:SS_CFPS_FY1_MEAN_DIFF1W2P = (CPS_FY1_MEAN_DIFF1W / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        cfps_fy1_mean_diff = self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="CFPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return cfps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_CFPS_FY1_MEAN_DIFF22D2P(self, field, **kwds_args):
        """SS_CFPS_FY1_MEAN_DIFF22D2P = (CPS_FY1_MEAN_DIFF22D / CLOSE)"""
        # FL:SS_CFPS_FY1_MEAN_DIFF22D2P = (CPS_FY1_MEAN_DIFF22D / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        cfps_fy1_mean_diff = self.get_est_chg(
            window_size=22,
            window_op="diff",
            metric="CFPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return cfps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_CFPS_FY1_MEAN_DIFF4W2P(self, field, **kwds_args):
        """SS_CFPS_FY1_MEAN_DIFF4W2P = (CPS_FY1_MEAN_DIFF4W / CLOSE)"""
        # FL:SS_CFPS_FY1_MEAN_DIFF4W2P = (CPS_FY1_MEAN_DIFF4W / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        cfps_fy1_mean_diff = self.get_est_chg(
            window_size=4,
            window_op="diff",
            metric="CFPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return cfps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_CFPS_FY1_MEAN_DIFF1M2P(self, field, **kwds_args):
        """SS_CFPS_FY1_MEAN_DIFF1M2P = (CPS_FY1_MEAN_DIFF1M / CLOSE)"""
        # FL:SS_CFPS_FY1_MEAN_DIFF1M2P = (CPS_FY1_MEAN_DIFF1M / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        cfps_fy1_mean_diff = self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="CFPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return cfps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_CFPS_FY1_MEAN_DIFF65D2P(self, field, **kwds_args):
        """SS_CFPS_FY1_MEAN_DIFF65D2P = (CPS_FY1_MEAN_DIFF65D / CLOSE)"""
        # FL:SS_CFPS_FY1_MEAN_DIFF65D2P = (CPS_FY1_MEAN_DIFF65D / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        cfps_fy1_mean_diff = self.get_est_chg(
            window_size=65,
            window_op="diff",
            metric="CFPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return cfps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_CFPS_FY1_MEAN_DIFF13W2P(self, field, **kwds_args):
        """SS_CFPS_FY1_MEAN_DIFF13W2P = (CPS_FY1_MEAN_DIFF13W / CLOSE)"""
        # FL:SS_CFPS_FY1_MEAN_DIFF13W2P = (CPS_FY1_MEAN_DIFF13W / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        cfps_fy1_mean_diff = self.get_est_chg(
            window_size=13,
            window_op="diff",
            metric="CFPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return cfps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_CFPS_FY1_MEAN_DIFF3M2P(self, field, **kwds_args):
        """SS_CFPS_FY1_MEAN_DIFF3M2P = (CPS_FY1_MEAN_DIFF3M / CLOSE)"""
        # FL:SS_CFPS_FY1_MEAN_DIFF3M2P = (CPS_FY1_MEAN_DIFF3M / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        cfps_fy1_mean_diff = self.get_est_chg(
            window_size=3,
            window_op="diff",
            metric="CFPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return cfps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_DPS_FY1_MEAN_DIFF5D2P(self, field, **kwds_args):
        """SS_DPS_FY1_MEAN_DIFF5D2P = (DPS_FY1_MEAN_DIFF5D / CLOSE)"""
        # FL:SS_DPS_FY1_MEAN_DIFF5D2P = (DPS_FY1_MEAN_DIFF5D / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        dps_fy1_mean_diff = self.get_est_chg(
            window_size=5,
            window_op="diff",
            metric="DPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return dps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_DPS_FY1_MEAN_DIFF1W2P(self, field, **kwds_args):
        """SS_DPS_FY1_MEAN_DIFF1W2P = (DPS_FY1_MEAN_DIFF1W / CLOSE)"""
        # FL:SS_DPS_FY1_MEAN_DIFF1W2P = (DPS_FY1_MEAN_DIFF1W / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        dps_fy1_mean_diff = self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="DPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return dps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_DPS_FY1_MEAN_DIFF22D2P(self, field, **kwds_args):
        """SS_DPS_FY1_MEAN_DIFF22D2P = (DPS_FY1_MEAN_DIFF22D / CLOSE)"""
        # FL:SS_DPS_FY1_MEAN_DIFF22D2P = (DPS_FY1_MEAN_DIFF22D / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        dps_fy1_mean_diff = self.get_est_chg(
            window_size=22,
            window_op="diff",
            metric="DPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return dps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_DPS_FY1_MEAN_DIFF4W2P(self, field, **kwds_args):
        """SS_DPS_FY1_MEAN_DIFF4W2P = (DPS_FY1_MEAN_DIFF4W / CLOSE)"""
        # FL:SS_DPS_FY1_MEAN_DIFF4W2P = (DPS_FY1_MEAN_DIFF4W / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        dps_fy1_mean_diff = self.get_est_chg(
            window_size=4,
            window_op="diff",
            metric="DPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return dps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_DPS_FY1_MEAN_DIFF1M2P(self, field, **kwds_args):
        """SS_DPS_FY1_MEAN_DIFF1M2P = (DPS_FY1_MEAN_DIFF1M / CLOSE)"""
        # FL:SS_DPS_FY1_MEAN_DIFF1M2P = (DPS_FY1_MEAN_DIFF1M / CLOSE)

        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        dps_fy1_mean_diff = self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="DPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        return dps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_DPS_FY1_MEAN_DIFF65D2P(self, field, **kwds_args):
        """SS_DPS_FY1_MEAN_DIFF65D2P = (DPS_FY1_MEAN_DIFF65D / CLOSE)"""
        # FL:SS_DPS_FY1_MEAN_DIFF65D2P = (DPS_FY1_MEAN_DIFF65D / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        dps_fy1_mean_diff = self.get_est_chg(
            window_size=65,
            window_op="diff",
            metric="DPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return dps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_DPS_FY1_MEAN_DIFF13W2P(self, field, **kwds_args):
        """SS_DPS_FY1_MEAN_DIFF13W2P = (DPS_FY1_MEAN_DIFF13W / CLOSE)"""
        # FL:SS_DPS_FY1_MEAN_DIFF13W2P = (DPS_FY1_MEAN_DIFF13W / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        dps_fy1_mean_diff = self.get_est_chg(
            window_size=13,
            window_op="diff",
            metric="DPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return dps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_DPS_FY1_MEAN_DIFF3M2P(self, field, **kwds_args):
        """SS_DPS_FY1_MEAN_DIFF3M2P = (DPS_FY1_MEAN_DIFF3M / CLOSE)"""
        # FL:SS_DPS_FY1_MEAN_DIFF3M2P = (DPS_FY1_MEAN_DIFF3M / CLOSE)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        dps_fy1_mean_diff = self.get_est_chg(
            window_size=3,
            window_op="diff",
            metric="DPS",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return dps_fy1_mean_diff / close

    @RootLib.temp_frame()
    def SS_ROE_FY1_MEAN_DIFF5D(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF5D = ROE_FY1_MEAN_DIFF5D"""
        # FL:SS_ROE_FY1_MEAN_DIFF5D = ROE_FY1_MEAN_DIFF5D
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=5,
            window_op="diff",
            metric="ROE",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_ROE_FY1_MEAN_DIFF1W(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF1W = ROE_FY1_MEAN_DIFF1W"""
        # FL:SS_ROE_FY1_MEAN_DIFF1W = ROE_FY1_MEAN_DIFF1W
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )

        return self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="ROE",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_ROE_FY1_MEAN_DIFF22D(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF22D = ROE_FY1_MEAN_DIFF22D"""
        # FL:SS_ROE_FY1_MEAN_DIFF22D = ROE_FY1_MEAN_DIFF22D
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=22,
            window_op="diff",
            metric="ROE",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_ROE_FY1_MEAN_DIFF4W(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF4W = ROE_FY1_MEAN_DIFF4W"""
        # FL:SS_ROE_FY1_MEAN_DIFF4W = ROE_FY1_MEAN_DIFF4W
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=4,
            window_op="diff",
            metric="ROE",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_ROE_FY1_MEAN_DIFF1M(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF1M = ROE_FY1_MEAN_DIFF1M"""
        # FL:SS_ROE_FY1_MEAN_DIFF1M = ROE_FY1_MEAN_DIFF1M
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="ROE",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_ROE_FY1_MEAN_DIFF65D(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF65D = ROE_FY1_MEAN_DIFF65D"""
        # FL:SS_ROE_FY1_MEAN_DIFF65D = ROE_FY1_MEAN_DIFF65D
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=65,
            window_op="diff",
            metric="ROE",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_ROE_FY1_MEAN_DIFF13W(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF13W = ROE_FY1_MEAN_DIFF13W"""
        # FL:SS_DPS_FY1_MEAN_DIFF13W = ROE_FY1_MEAN_DIFF13W
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=13,
            window_op="diff",
            metric="ROE",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_ROE_FY1_MEAN_DIFF3M(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF3M = ROE_FY1_MEAN_DIFF3M"""
        # FL:SS_DPS_FY1_MEAN_DIFF3M = ROE_FY1_MEAN_DIFF3M
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=3,
            window_op="diff",
            metric="ROE",
            prd="FY1",
            stat="MEAN",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_MV2NUM(self, field, **kwds_args):
        # FL:SS_MV2NUM = (MKTCAP/EPS_FY1_NUM)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        est_fy1_num = self.get_calendarized_field(
            field_prefix="EPS_FY1_NUM", freq=freq, lib=est_summary_lib
        )
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        # Require positive num
        est_fy1_num.conditional_nullify_inplace(est_fy1_num <= 0)

        return mv / est_fy1_num

    @RootLib.temp_frame()
    def SS_MV2NUM_PCHG22D(self, field, **kwds_args):
        # FL:SS_MV2NUM_PCHG22D = MPCTCHG(SS_MV2NUM,22)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        est_fy1_num = self.get_calendarized_field(
            field_prefix="EPS_FY1_NUM", freq=freq, lib=est_summary_lib
        )
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)

        # Require positive num
        est_fy1_num.conditional_nullify_inplace(est_fy1_num <= 0)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        mv2num = mv / est_fy1_num
        return mv2num.mpctchg1d(22, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_MV2NUM_PCHG4W(self, field, **kwds_args):
        # FL:SS_MV2NUM_PCHG4W = MPCTCHG(SS_MV2NUM,4)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        est_fy1_num = self.get_calendarized_field(
            field_prefix="EPS_FY1_NUM", freq=freq, lib=est_summary_lib
        )
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)

        # Require positive num
        est_fy1_num.conditional_nullify_inplace(est_fy1_num <= 0)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        mv2num = mv / est_fy1_num
        return mv2num.mpctchg1d(4, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_MV2NUM_PCHG1M(self, field, **kwds_args):
        # FL:SS_MV2NUM_PCHG1M = MPCTCHG(SS_MV2NUM,1)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        est_fy1_num = self.get_calendarized_field(
            field_prefix="EPS_FY1_NUM", freq=freq, lib=est_summary_lib
        )
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)

        # Require positive num
        est_fy1_num.conditional_nullify_inplace(est_fy1_num <= 0)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        mv2num = mv / est_fy1_num
        return mv2num.mpctchg1d(1, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_MV2NUM_PCHG65D(self, field, **kwds_args):
        # FL:SS_MV2NUM_PCHG65D = MPCTCHG(SS_MV2NUM,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        est_fy1_num = self.get_calendarized_field(
            field_prefix="EPS_FY1_NUM", freq=freq, lib=est_summary_lib
        )
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)

        # Require positive num
        est_fy1_num.conditional_nullify_inplace(est_fy1_num <= 0)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        mv2num = mv / est_fy1_num
        return mv2num.mpctchg1d(65, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_MV2NUM_PCHG13W(self, field, **kwds_args):
        # FL:SS_MV2NUM_PCHG13W = MPCTCHG(SS_MV2NUM,13)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        est_fy1_num = self.get_calendarized_field(
            field_prefix="EPS_FY1_NUM", freq=freq, lib=est_summary_lib
        )
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)

        # Require positive num
        est_fy1_num.conditional_nullify_inplace(est_fy1_num <= 0)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        mv2num = mv / est_fy1_num
        return mv2num.mpctchg1d(13, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_MV2NUM_PCHG3M(self, field, **kwds_args):
        # FL:SS_MV2NUM_PCHG3M = MPCTCHG(SS_MV2NUM,3)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        est_fy1_num = self.get_calendarized_field(
            field_prefix="EPS_FY1_NUM", freq=freq, lib=est_summary_lib
        )
        mv = self.get_calendarized_field(field_prefix="MKTCAP", freq=freq, lib=self)

        # Require positive num
        est_fy1_num.conditional_nullify_inplace(est_fy1_num <= 0)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        mv2num = mv / est_fy1_num
        return mv2num.mpctchg1d(3, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_NUM_DIFF22D(self, field, **kwds_args):
        # FL:SS_NUM_DIFF22D = EPS_FY1_NUM_DIFF22D
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=22,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="NUM",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_NUM_DIFF4W(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF4W = ROE_FY1_MEAN_DIFF4W"""
        # FL:SS_ROE_FY1_MEAN_DIFF4W = ROE_FY1_MEAN_DIFF4W
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=4,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="NUM",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_NUM_DIFF1M(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF1M = ROE_FY1_MEAN_DIFF1M"""
        # FL:SS_ROE_FY1_MEAN_DIFF1M = ROE_FY1_MEAN_DIFF1M
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=1,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="NUM",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_NUM_DIFF65D(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF65D = ROE_FY1_MEAN_DIFF65D"""
        # FL:SS_ROE_FY1_MEAN_DIFF65D = ROE_FY1_MEAN_DIFF65D
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=65,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="NUM",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_NUM_DIFF13W(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF13W = ROE_FY1_MEAN_DIFF13W"""
        # FL:SS_DPS_FY1_MEAN_DIFF13W = ROE_FY1_MEAN_DIFF13W
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=13,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="NUM",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_NUM_DIFF3M(self, field, **kwds_args):
        """SS_ROE_FY1_MEAN_DIFF3M = ROE_FY1_MEAN_DIFF3M"""
        # FL:SS_DPS_FY1_MEAN_DIFF3M = ROE_FY1_MEAN_DIFF3M
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_est_chg(
            window_size=3,
            window_op="diff",
            metric="EPS",
            prd="FY1",
            stat="NUM",
            freq=freq,
            lib=est_summary_lib,
            dates_keyspace=dates_keyspace,
            add_frame=False,
        )

    @RootLib.temp_frame()
    def SS_EPS_DISP2P(self, field, **kwds_args):
        """SS_EPS_DISP2P: Sell-Side 1Yr Forward EPS Dispersion (aka StdDev) / Price
        (Wtd Ave of FY1 EPS STDDEV & FY2 EPS STDDEV) / Price
        Where weights are based on fraction of year remaining in FY1 & complementary FY2
        DIRECTION: BULLISH (Non-Perverse: High Dispersion = Higher Uncertianty = Higher Risk which Commands Higher Returns)
        IMPORTANT NOTE: Many quants merely define this factors "Raw" EPS Dispersion (without normalizing by Price/Share)
                        I chose not to do this, because without normalization, the "high dispersion" conditions
                        will be biased/dominated by higher priced stocks...resulting in a unintentional size bias/
                        Normalizing the level of EPS Dispersion by the Price/Share protects against this size bias in the factor.
                        The un-normalized/common definition is perverse (High Raw Dispersion stocks UNDEPERFORM),
                        whereas the normalized definition is not-perverse (High Raw Dispersion stocks OUTPERFORM)
        """
        # DL:SS_EPS_DISP2P = SS_EPS_FWD1Y_DISP / CLOSE
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        eps_fwd1y_disp = self.EST_FWD1Y(
            field=field,
            freq=freq,
            est_category_name="EPS",
            est_stats_name="STDDEV",
            est_summary_lib=est_summary_lib,
            est_dates_keyspace=dates_keyspace,
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return eps_fwd1y_disp / close

    @RootLib.temp_frame()
    def SS_PTG_MEAN2P(self, field, **kwds_args):
        """SS_PTG_MEAN2P: Sell-Side (Mean Price Target / Price) = (PTG_MEAN/CLOSE)"""
        # FL:SS_PTG_MEAN2P = (PTG_MEAN / CLOSE)
        # <-- Could have called this: SS_PTG_MEAN2P
        prc_lib = self.get_property("prc_lib", field, grace=False)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        ptg_mean = self.get_calendarized_field(
            field_prefix="PTG_MEAN", freq=freq, lib=est_summary_lib
        )

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return ptg_mean / close

    @RootLib.temp_frame()
    def SS_PTG_MEAN_PCHG5D(self, field, **kwds_args):
        """SS_PTG_MEAN_PCHG5D: 5-Day PctChg in Mean Target Price"""
        # FL:SS_PTG_MEAN_PCHG5D = MPCTCHG(PTG_MEAN,5)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="PTG_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(5, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_PTG_MEAN_PCHG1W(self, field, **kwds_args):
        """SS_PTG_MEAN_PCHG5D: 1 Week PctChg in Mean Target Price"""
        # FL:SS_PTG_MEAN_PCHG5D = MPCTCHG(PTG_MEAN,1)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )

        return self.get_calendarized_field(
            field_prefix="PTG_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(1, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_PTG_MEAN_PCHG22D(self, field, **kwds_args):
        """SS_PTG_MEAN_PCHG22D: 22-Day PctChg in Mean Target Price"""
        # FL:SS_PTG_MEAN_PCHG22D = MPCTCHG(PTG_MEAN,22)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="PTG_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(22, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_PTG_MEAN_PCHG4W(self, field, **kwds_args):
        """SS_PTG_MEAN_PCHG22D: 4-Week PctChg in Mean Target Price"""
        # FL:SS_PTG_MEAN_PCHG22D = MPCTCHG(PTG_MEAN,4)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="PTG_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(4, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_PTG_MEAN_PCHG1M(self, field, **kwds_args):
        """SS_PTG_MEAN_PCHG22D: 1-Month PctChg in Mean Target Price"""
        # FL:SS_PTG_MEAN_PCHG22D = MPCTCHG(PTG_MEAN,1)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="PTG_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(1, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_PTG_MEAN_PCHG65D(self, field, **kwds_args):
        """SS_PTG_MEAN_PCHG65D: 65-Day PctChg in Mean Target Price"""
        # FL:SS_PTG_MEAN_PCHG65D = MPCTCHG(PTG_MEAN,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="PTG_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(65, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_PTG_MEAN_PCHG13W(self, field, **kwds_args):
        """SS_PTG_MEAN_PCHG13W: 13-Week PctChg in Mean Target Price"""
        # FL:SS_PTG_MEAN_PCHG65D = MPCTCHG(PTG_MEAN,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="PTG_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(13, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_PTG_MEAN_PCHG3M(self, field, **kwds_args):
        """SS_PTG_MEAN_PCHG3M: 3-Month PctChg in Mean Target Price"""
        # FL:SS_PTG_MEAN_PCHG65D = MPCTCHG(PTG_MEAN,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="PTG_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(3, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_NAV_FY1_MEAN_PCHG5D(self, field, **kwds_args):
        """SS_NAV_FY1_MEAN_PCHG5D: 5-Day PctChg in Mean NAV FY1 Estimate"""
        # FL:SS_NAV_FY1_MEAN_PCHG5D = MPCTCHG(NAV_FY1_MEAN,5)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="NAV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(5, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_NAV_FY1_MEAN_PCHG1W(self, field, **kwds_args):
        """SS_NAV_FY1_MEAN_PCHG5D: 1 Week PctChg in Mean NAV FY1 Estimate"""
        # FL:SS_NAV_FY1_MEAN_PCHG5D = MPCTCHG(NAV_FY1_MEAN,1)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="NAV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(1, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_NAV_FY1_MEAN_PCHG22D(self, field, **kwds_args):
        """SS_NAV_FY1_MEAN_PCHG22D: 22-Day PctChg in Mean NAV FY1 Estimate"""
        # FL:SS_NAV_FY1_MEAN_PCHG22D = MPCTCHG(NAV_FY1_MEAN,22)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="NAV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(22, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_NAV_FY1_MEAN_PCHG4W(self, field, **kwds_args):
        """SS_NAV_FY1_MEAN_PCHG22D: 4-Week PctChg in Mean NAV FY1 Estimate"""
        # FL:SS_NAV_FY1_MEAN_PCHG22D = MPCTCHG(NAV_FY1_MEAN,4)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="NAV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(4, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_NAV_FY1_MEAN_PCHG1M(self, field, **kwds_args):
        """SS_NAV_FY1_MEAN_PCHG22D: 1-Month PctChg in Mean NAV FY1 Estimate"""
        # FL:SS_NAV_FY1_MEAN_PCHG22D = MPCTCHG(NAV_FY1_MEAN,1)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="NAV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(1, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_NAV_FY1_MEAN_PCHG65D(self, field, **kwds_args):
        """SS_NAV_FY1_MEAN_PCHG65D: 65-Day PctChg in Mean NAV FY1 Estimate"""
        # FL:SS_NAV_FY1_MEAN_PCHG65D = MPCTCHG(NAV_FY1_MEAN,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="NAV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(65, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_NAV_FY1_MEAN_PCHG13W(self, field, **kwds_args):
        """SS_NAV_FY1_MEAN_PCHG13W: 13-Week PctChg in Mean NAV FY1 Estimate"""
        # FL:SS_NAV_FY1_MEAN_PCHG65D = MPCTCHG(NAV_FY1_MEAN,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="NAV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(13, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_NAV_FY1_MEAN_PCHG3M(self, field, **kwds_args):
        """SS_NAV_FY1_MEAN_PCHG3M: 3-Month PctChg in Mean NAV FY1 Estimate"""
        # FL:SS_NAV_FY1_MEAN_PCHG65D = MPCTCHG(NAV_FY1_MEAN,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="NAV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(3, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_PCHG5D(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_PCHG5D: 5-Day PctChg in Mean SALES FY1 Estimate"""
        # FL:SS_SALES_FY1_MEAN_PCHG5D = MPCTCHG(REV_FY1_MEAN,5)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(5, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_PCHG1W(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_PCHG5D: 1 Week PctChg in Mean SALES FY1 Estimate"""
        # FL:SS_SALES_FY1_MEAN_PCHG5D = MPCTCHG(REV_FY1_MEAN,1)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(1, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_PCHG22D(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_PCHG22D: 22-Day PctChg in Mean SALES FY1 Estimate"""
        # FL:SS_SALES_FY1_MEAN_PCHG22D = MPCTCHG(REV_FY1_MEAN,22)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(22, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_PCHG4W(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_PCHG22D: 4-Week PctChg in Mean SALES FY1 Estimate"""
        # FL:SS_SALES_FY1_MEAN_PCHG22D = MPCTCHG(REV_FY1_MEAN,4)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(4, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_PCHG1M(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_PCHG22D: 1-Month PctChg in Mean SALES FY1 Estimate"""
        # FL:SS_SALES_FY1_MEAN_PCHG22D = MPCTCHG(REV_FY1_MEAN,1)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(1, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_PCHG65D(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_PCHG65D: 65-Day PctChg in Mean SALES FY1 Estimate"""
        # FL:SS_SALES_FY1_MEAN_PCHG65D = MPCTCHG(REV_FY1_MEAN,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(65, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_PCHG13W(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_PCHG13W: 13-Week PctChg in Mean SALES FY1 Estimate"""
        # FL:SS_SALES_FY1_MEAN_PCHG65D = MPCTCHG(REV_FY1_MEAN,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(13, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_SALES_FY1_MEAN_PCHG3M(self, field, **kwds_args):
        """SS_SALES_FY1_MEAN_PCHG3M: 3-Month PctChg in Mean SALES FY1 Estimate"""
        # FL:SS_SALES_FY1_MEAN_PCHG65D = MPCTCHG(REV_FY1_MEAN,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REV_FY1_MEAN", freq=freq, lib=est_summary_lib
        ).mpctchg1d(3, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_REC_MEAN(self, field, **kwds_args):
        """SS_REC_MEAN: Sell-Side Mean Recommendation
        Using TR REC SCALE:1=Strong Buy,2=Buy,3=Hold,4=Underperform,5=Sell
        """
        # FL:SS_RCMD_MEAN = REC_MEAN
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq is not None:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REC_MEAN", freq=freq, lib=est_summary_lib
        )

    @RootLib.temp_frame()
    def SS_REC_MEAN_DIFF5D(self, field, **kwds_args):
        """SS_REC_MEAN_DIFF5D: 5-Day Difference in Mean Recommendation"""
        # FL:SS_REC_MEAN_DIFF5D = MDIFF(REC_MEAN,5)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REC_MEAN", freq=freq, lib=est_summary_lib
        ).mdiff1d(5, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_REC_MEAN_DIFF1W(self, field, **kwds_args):
        """SS_REC_MEAN_DIFF1W: 1-Week Difference in Mean Recommendation"""
        # FL:SS_REC_MEAN_DIFF1W = MDIFF(REC_MEAN,1)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REC_MEAN", freq=freq, lib=est_summary_lib
        ).mdiff1d(1, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_REC_MEAN_DIFF22D(self, field, **kwds_args):
        """SS_REC_MEAN_DIFF22D: 22-Day Difference in Mean Recommendation"""
        # FL:SS_REC_MEAN_DIFF22D = MDIFF(REC_MEAN,22)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REC_MEAN", freq=freq, lib=est_summary_lib
        ).mdiff1d(22, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_REC_MEAN_DIFF4W(self, field, **kwds_args):
        """SS_REC_MEAN_DIFF4W: 4-Week Difference in Mean Recommendation"""
        # FL:SS_REC_MEAN_DIFF4W = MDIFF(REC_MEAN,4)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REC_MEAN", freq=freq, lib=est_summary_lib
        ).mdiff1d(4, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_REC_MEAN_DIFF1M(self, field, **kwds_args):
        """SS_REC_MEAN_DIFF1M: 1-Month Difference in Mean Recommendation"""
        # FL:SS_REC_MEAN_DIFF1M = MDIFF(REC_MEAN,1)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REC_MEAN", freq=freq, lib=est_summary_lib
        ).mdiff1d(1, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_REC_MEAN_DIFF65D(self, field, **kwds_args):
        """SS_REC_MEAN_DIFF65D: 65-Day Difference in Mean Recommendation"""
        # FL:SS_REC_MEAN_DIFF65D = MDIFF(REC_MEAN,65)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "WEEKDAY":
            raise Exception(f"Invalid freq:{freq}...Expected: 'WEEKDAY'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REC_MEAN", freq=freq, lib=est_summary_lib
        ).mdiff1d(65, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_REC_MEAN_DIFF13W(self, field, **kwds_args):
        """SS_REC_MEAN_DIFF13W: 13-Week Difference in Mean Recommendation"""
        # FL:SS_REC_MEAN_DIFF13W = MDIFF(REC_MEAN,13)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq not in ("W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"):
            raise Exception(
                "Invalid freq:{0}...Expected: 'W@MON' or 'W@TUE' or 'W@WED' or 'W@THU' or 'W@FRI'".format(
                    freq
                )
            )
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REC_MEAN", freq=freq, lib=est_summary_lib
        ).mdiff1d(13, keyspace=dates_keyspace)

    @RootLib.temp_frame()
    def SS_REC_MEAN_DIFF3M(self, field, **kwds_args):
        """SS_REC_MEAN_DIFF3M: 3-Month Difference in Mean Recommendation"""
        # FL:SS_REC_MEAN_DIFF3M = MDIFF(REC_MEAN,3)
        est_summary_lib = self.get_property("est_summary_lib", field, grace=False)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        if freq != "CEOM":
            raise Exception(f"Invalid freq:{freq}...Expected: 'CEOM'")
        else:
            RootLib().set_control("freq", freq)

        return self.get_calendarized_field(
            field_prefix="REC_MEAN", freq=freq, lib=est_summary_lib
        ).mdiff1d(3, keyspace=dates_keyspace)

    # ============================ TECHNICAL OSCILLATORS ==============================

    def _cume_return(
        self, field, periods, lag, valid_freqs, add_frame=False, **kwds_args
    ):
        if add_frame:
            RootLib.add_frame()

        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        if not isinstance(valid_freqs, (list, tuple)):
            valid_freqs = [valid_freqs]

        if freq not in valid_freqs:
            raise Exception("Invalid freq:{0}...Expected: {0}".format(valid_freqs))
        else:
            RootLib().set_control("freq", freq)

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        pct_ret = (
            close / close.shift1d(periods=periods, keyspace=dates_keyspace)
        ) - 1.0
        if lag != 0:
            pct_ret = pct_ret.shift1d(periods=lag, keyspace=dates_keyspace)

        if add_frame:
            RootLib.pop_frame()

        return pct_ret

    def daily_cume_return(self, field, periods, lag=0, add_frame=False, **kwds_args):
        return self._cume_return(
            field=field,
            periods=periods,
            lag=lag,
            valid_freqs=["WEEKDAY"],
            add_frame=add_frame,
            **kwds_args,
        )

    def weekly_cume_return(self, field, periods, lag=0, add_frame=False, **kwds_args):
        return self._cume_return(
            field=field,
            periods=periods,
            lag=lag,
            valid_freqs=["W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"],
            add_frame=add_frame,
            **kwds_args,
        )

    def monthly_cume_return(self, field, periods, lag=0, add_frame=False, **kwds_args):
        return self._cume_return(
            field=field,
            periods=periods,
            lag=lag,
            valid_freqs=["CEOM"],
            add_frame=add_frame,
            **kwds_args,
        )

    def _p2high_or_low(
        self, field, periods, high_or_low, valid_freqs, add_frame=False, **kwds_args
    ):
        if add_frame:
            RootLib.add_frame()

        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        if not isinstance(valid_freqs, (list, tuple)):
            valid_freqs = [valid_freqs]

        if freq not in valid_freqs:
            raise Exception("Invalid freq:{0}...Expected: {0}".format(valid_freqs))
        else:
            RootLib().set_control("freq", freq)

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        if high_or_low == "high":
            close_mhigh = close.mmax1d(
                periods=periods,
                keyspace=dates_keyspace,
                pct_required=0.5,
                ignore_missing=True,
            )
            result = close / close_mhigh
        elif high_or_low == "low":
            close_mlow = close.mmin1d(
                periods=periods,
                keyspace=dates_keyspace,
                pct_required=0.5,
                ignore_missing=True,
            )
            result = close / close_mlow
        else:
            raise Exception(
                f"Invalid high_or_low:{high_or_low}...Expected: 'high' or 'low'"
            )

        if add_frame:
            RootLib.pop_frame()

        return result

    def daily_p2high(self, field, periods, add_frame=False, **kwds_args):
        return self._p2high_or_low(
            field=field,
            periods=periods,
            high_or_low="high",
            valid_freqs=["WEEKDAY"],
            add_frame=add_frame,
        )

    def weekly_p2high(self, field, periods, add_frame=False, **kwds_args):
        return self._p2high_or_low(
            field=field,
            periods=periods,
            high_or_low="high",
            valid_freqs=["W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"],
            add_frame=add_frame,
        )

    def monthly_p2high(self, field, periods, add_frame=False, **kwds_args):
        return self._p2high_or_low(
            field=field,
            periods=periods,
            high_or_low="high",
            valid_freqs=["CEOM"],
            add_frame=add_frame,
        )

    def daily_p2low(self, field, periods, add_frame=False, **kwds_args):
        return self._p2high_or_low(
            field=field,
            periods=periods,
            high_or_low="low",
            valid_freqs=["WEEKDAY"],
            add_frame=add_frame,
        )

    def weekly_p2low(self, field, periods, add_frame=False, **kwds_args):
        return self._p2high_or_low(
            field=field,
            periods=periods,
            high_or_low="low",
            valid_freqs=["W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"],
            add_frame=add_frame,
        )

    def monthly_p2low(self, field, periods, add_frame=False, **kwds_args):
        return self._p2high_or_low(
            field=field,
            periods=periods,
            high_or_low="low",
            valid_freqs=["CEOM"],
            add_frame=add_frame,
        )

    def _price_mave_ratio(
        self,
        field,
        short_periods,
        long_periods,
        valid_freqs,
        add_frame=False,
        **kwds_args,
    ):
        if add_frame:
            RootLib.add_frame()

        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        if not isinstance(valid_freqs, (list, tuple)):
            valid_freqs = [valid_freqs]

        if freq not in valid_freqs:
            raise Exception("Invalid freq:{0}...Expected: {0}".format(valid_freqs))
        else:
            RootLib().set_control("freq", freq)

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        short_mave = close.mmean1d(
            periods=short_periods,
            keyspace=dates_keyspace,
            pct_required=0.5,
            ignore_missing=True,
        )
        long_mave = close.mmean1d(
            periods=long_periods,
            keyspace=dates_keyspace,
            pct_required=0.5,
            ignore_missing=True,
        )
        result = short_mave / long_mave

        if add_frame:
            RootLib.pop_frame()

        return result

    def daily_price_mave_ratio(
        self, field, short_periods, long_periods, add_frame=False, **kwds_args
    ):
        return self._price_mave_ratio(
            field=field,
            short_periods=short_periods,
            long_periods=long_periods,
            valid_freqs=["WEEKDAY"],
            add_frame=add_frame,
        )

    def weekly_price_mave_ratio(
        self, field, short_periods, long_periods, add_frame=False, **kwds_args
    ):
        return self._price_mave_ratio(
            field=field,
            short_periods=short_periods,
            long_periods=long_periods,
            valid_freqs=["W@MON", "W@TUE", "W@WED", "W@THU", "W@FRI"],
            add_frame=add_frame,
        )

    def monthly_price_mave_ratio(
        self, field, short_periods, long_periods, add_frame=False, **kwds_args
    ):
        return self._price_mave_ratio(
            field=field,
            short_periods=short_periods,
            long_periods=long_periods,
            valid_freqs=["CEOM"],
            add_frame=add_frame,
        )

    # SIMPLE TRAILING RETURN FACTORS...
    # -----------------------------------
    @RootLib.temp_frame()
    def RET1D(self, field, **kwds_args):
        """Trailing Return (Past 1D)"""
        # FL:RET1D = ((CLOSE(T)/CLOSE(T-1BD)) - 1)
        return self.daily_cume_return(field=field, periods=1, **kwds_args)

    @RootLib.temp_frame()
    def RET5D(self, field, **kwds_args):
        """Trailing Return (Past 5D)"""
        # FL:RET5D = ((CLOSE(T)/CLOSE(T-5BD)) - 1)
        return self.daily_cume_return(field=field, periods=5, **kwds_args)

    @RootLib.temp_frame()
    def RET1W(self, field, **kwds_args):
        """Trailing Return (Past 1W)"""
        # FL:RET5D = ((CLOSE(T)/CLOSE(T-1W)) - 1)
        return self.weekly_cume_return(field=field, periods=1, **kwds_args)

    @RootLib.temp_frame()
    def RET22D(self, field, **kwds_args):
        """Trailing Return (Past 22BD)"""
        # FL:RET22D = ((CLOSE(T)/CLOSE(T-22BD)) - 1)
        return self.daily_cume_return(field=field, periods=22, **kwds_args)

    @RootLib.temp_frame()
    def RET4W(self, field, **kwds_args):
        """Trailing Return (Past 4 Weeks)"""
        # FL:RET4W = ((CLOSE(T)/CLOSE(T-4W)) - 1)
        return self.weekly_cume_return(field=field, periods=4, **kwds_args)

    @RootLib.temp_frame()
    def RET1M(self, field, **kwds_args):
        """Trailing Return (Past 1M)"""
        # FL:RET1M = ((CLOSE(T)/CLOSE(T-1M)) - 1)
        return self.monthly_cume_return(field=field, periods=1, **kwds_args)

    @RootLib.temp_frame()
    def RET65D(self, field, **kwds_args):
        """Trailing Return (Past 65BD)"""
        # FL:RET65D = ((CLOSE(T)/CLOSE(T-65BD)) - 1)
        return self.daily_cume_return(field=field, periods=65, **kwds_args)

    @RootLib.temp_frame()
    def RET13W(self, field, **kwds_args):
        """Trailing Return (Past 13 Weeks)"""
        # FL:RET13W = ((CLOSE(T)/CLOSE(T-13W)) - 1)
        return self.weekly_cume_return(field=field, periods=13, **kwds_args)

    @RootLib.temp_frame()
    def RET3M(self, field, **kwds_args):
        """Trailing Return (Past 3M)"""
        # FL:RET3M = ((CLOSE(T)/CLOSE(T-3M)) - 1)
        return self.monthly_cume_return(field=field, periods=3, **kwds_args)

    @RootLib.temp_frame()
    def RET130D(self, field, **kwds_args):
        """Trailing Return (Past 130BD)"""
        # FL:RET130D = ((CLOSE(T)/CLOSE(T-130BD)) - 1)
        return self.daily_cume_return(field=field, periods=130, **kwds_args)

    @RootLib.temp_frame()
    def RET26W(self, field, **kwds_args):
        """Trailing Return (Past 26 Weeks)"""
        # FL:RET26W = ((CLOSE(T)/CLOSE(T-26W)) - 1)
        return self.weekly_cume_return(field=field, periods=26, **kwds_args)

    @RootLib.temp_frame()
    def RET6M(self, field, **kwds_args):
        """Trailing Return (Past 6M)"""
        # FL:RET6M = ((CLOSE(T)/CLOSE(T-6M)) - 1)
        return self.monthly_cume_return(field=field, periods=6, **kwds_args)

    @RootLib.temp_frame()
    def RET196D(self, field, **kwds_args):
        """Trailing Return (Past 196BD)"""
        # FL:RET196D = ((CLOSE(T)/CLOSE(T-196BD)) - 1)
        return self.daily_cume_return(field=field, periods=196, **kwds_args)

    @RootLib.temp_frame()
    def RET39W(self, field, **kwds_args):
        """Trailing Return (Past 39 Weeks)"""
        # FL:RET39W = ((CLOSE(T)/CLOSE(T-39W)) - 1)
        return self.weekly_cume_return(field=field, periods=39, **kwds_args)

    @RootLib.temp_frame()
    def RET9M(self, field, **kwds_args):
        """Trailing Return (Past 9M)"""
        # FL:RET9M = ((CLOSE(T)/CLOSE(T-9M)) - 1)
        return self.monthly_cume_return(field=field, periods=9, **kwds_args)

    @RootLib.temp_frame()
    def RET261D(self, field, **kwds_args):
        """Trailing Return (Past 261BD)"""
        # FL:RET261D = ((CLOSE(T)/CLOSE(T-261BD)) - 1)
        return self.daily_cume_return(field=field, periods=261, **kwds_args)

    @RootLib.temp_frame()
    def RET52W(self, field, **kwds_args):
        """Trailing Return (Past 52 Weeks)"""
        # FL:RET52W = ((CLOSE(T)/CLOSE(T-52W)) - 1)
        return self.weekly_cume_return(field=field, periods=52, **kwds_args)

    @RootLib.temp_frame()
    def RET12M(self, field, **kwds_args):
        """Trailing Return (Past 12M)"""
        # FL:RET12M = ((CLOSE(T)/CLOSE(T-12M)) - 1)
        return self.monthly_cume_return(field=field, periods=12, **kwds_args)

    @RootLib.temp_frame()
    def RET392D(self, field, **kwds_args):
        """Trailing Return (Past 392BD)"""
        # FL:RET392D = ((CLOSE(T)/CLOSE(T-392BD)) - 1)
        return self.daily_cume_return(field=field, periods=392, **kwds_args)

    @RootLib.temp_frame()
    def RET78W(self, field, **kwds_args):
        """Trailing Return (Past 78 Weeks)"""
        # FL:RET78W = ((CLOSE(T)/CLOSE(T-78W)) - 1)
        return self.weekly_cume_return(field=field, periods=78, **kwds_args)

    @RootLib.temp_frame()
    def RET18M(self, field, **kwds_args):
        """Trailing Return (Past 18M)"""
        # FL:RET18M = ((CLOSE(T)/CLOSE(T-18M)) - 1)
        return self.monthly_cume_return(field=field, periods=18, **kwds_args)

    @RootLib.temp_frame()
    def RET783D(self, field, **kwds_args):
        """Trailing Return (Past 783BD)"""
        # FL:RET7832D = ((CLOSE(T)/CLOSE(T-783BD)) - 1)
        return self.daily_cume_return(field=field, periods=783, **kwds_args)

    @RootLib.temp_frame()
    def RET156W(self, field, **kwds_args):
        """Trailing Return (Past 156 Weeks)"""
        # FL:RET156W = ((CLOSE(T)/CLOSE(T-156W)) - 1)
        return self.weekly_cume_return(field=field, periods=156, **kwds_args)

    @RootLib.temp_frame()
    def RET36M(self, field, **kwds_args):
        """Trailing Return (Past 36M)"""
        # FL:RET36M = ((CLOSE(T)/CLOSE(T-36M)) - 1)
        return self.monthly_cume_return(field=field, periods=36, **kwds_args)

    # SIMPLE TRAILING DAILY RETURN FACTORS LAGGED 1 DBAY...
    # -------------------------------------------------------
    @RootLib.temp_frame()
    def RET1D_LAG1D(self, field, **kwds_args):
        """Trailing Return (Past 1BD) Lagged 1BD"""
        # FL:RET1D_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-1)) - 1BD),1BD)
        return self.daily_cume_return(field=field, periods=1, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET5D_LAG1D(self, field, **kwds_args):
        """Trailing Return (Past 5BD) Lagged 1BD"""
        # FL:RET5D_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-5BD)) - 1),1BD)
        return self.daily_cume_return(field=field, periods=5, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET22D_LAG1D(self, field, **kwds_args):
        """Trailing Return (Past 1M=Past 22BD) Lagged 1BD"""
        # FL:RET1M_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-22BD)) - 1),1BD)
        return self.daily_cume_return(field=field, periods=22, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET65D_LAG1D(self, field, **kwds_args):
        """Trailing Return (Past 3M=Past 65BD) Lagged 1BD"""
        # FL:RET3M_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-65BD)) - 1),1BD)
        return self.daily_cume_return(field=field, periods=65, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET130D_LAG1D(self, field, **kwds_args):
        """Trailing Return (Past 6M=Past 130BD) Lagged 1BD"""
        # FL:RET130D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-130BD)) - 1),1BD)
        return self.daily_cume_return(field=field, periods=130, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET196D_LAG1D(self, field, **kwds_args):
        """Trailing Return (Past 9M=Past 196BD) Lagged 1BD"""
        # FL:RET196D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-196BD)) - 1),1BD)
        return self.daily_cume_return(field=field, periods=196, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET261D_LAG1D(self, field, **kwds_args):
        """Trailing Return (Past 12M=Past 261BD) Lagged 1BD"""
        # FL:RET261D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-261BD)) - 1),1BD)
        return self.daily_cume_return(field=field, periods=261, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET392D_LAG1D(self, field, **kwds_args):
        """Trailing Return (Past 18M=Past 392BD) Lagged 1BD"""
        # FL:RET392D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-392BD)) - 1),1BD)
        return self.daily_cume_return(field=field, periods=392, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET783D_LAG1D(self, field, **kwds_args):
        """Trailing Return (Past 36M=Past 3*261BD=Past 783BD) Lagged 1BD"""
        # FL:RET36M_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-783BD)) - 1),1BD)
        return self.daily_cume_return(field=field, periods=783, lag=1, **kwds_args)

    # SIMPLE TRAILING DAILY RETURN FACTORS LAGGED 5 BDAYS...
    # -------------------------------------------------------
    @RootLib.temp_frame()
    def RET1D_LAG5D(self, field, **kwds_args):
        """Trailing Return (Past 1BD) Lagged 5BD"""
        # FL:RET1D_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-1)) - 1BD),5BD)
        return self.daily_cume_return(field=field, periods=1, lag=5, **kwds_args)

    @RootLib.temp_frame()
    def RET5D_LAG5D(self, field, **kwds_args):
        """Trailing Return (Past 5BD) Lagged 5BD"""
        # FL:RET5D_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-5BD)) - 1),5BD)
        return self.daily_cume_return(field=field, periods=5, lag=5, **kwds_args)

    @RootLib.temp_frame()
    def RET22D_LAG5D(self, field, **kwds_args):
        """Trailing Return (Past 1M=Past 22BD) Lagged 5BD"""
        # FL:RET1M_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-22BD)) - 1),5BD)
        return self.daily_cume_return(field=field, periods=22, lag=5, **kwds_args)

    @RootLib.temp_frame()
    def RET65D_LAG5D(self, field, **kwds_args):
        """Trailing Return (Past 3M=Past 65BD) Lagged 5BD"""
        # FL:RET3M_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-65BD)) - 5),1BD)
        return self.daily_cume_return(field=field, periods=65, lag=5, **kwds_args)

    @RootLib.temp_frame()
    def RET130D_LAG5D(self, field, **kwds_args):
        """Trailing Return (Past 6M=Past 130BD) Lagged 5BD"""
        # FL:RET130D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-130BD)) - 1),5BD)
        return self.daily_cume_return(field=field, periods=130, lag=5, **kwds_args)

    @RootLib.temp_frame()
    def RET196D_LAG5D(self, field, **kwds_args):
        """Trailing Return (Past 9M=Past 196BD) Lagged 5BD"""
        # FL:RET196D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-196BD)) - 1),5BD)
        return self.daily_cume_return(field=field, periods=196, lag=5, **kwds_args)

    @RootLib.temp_frame()
    def RET261D_LAG5D(self, field, **kwds_args):
        """Trailing Return (Past 12M=Past 261BD) Lagged 5BD"""
        # FL:RET261D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-261BD)) - 1),5BD)
        return self.daily_cume_return(field=field, periods=261, lag=5, **kwds_args)

    @RootLib.temp_frame()
    def RET392D_LAG5D(self, field, **kwds_args):
        """Trailing Return (Past 18M=Past 392BD) Lagged 5BD"""
        # FL:RET392D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-392BD)) - 1),5BD)
        return self.daily_cume_return(field=field, periods=392, lag=5, **kwds_args)

    @RootLib.temp_frame()
    def RET783D_LAG5D(self, field, **kwds_args):
        """Trailing Return (Past 36M=Past 3*261BD=Past 783BD) Lagged 5BD"""
        # FL:RET36M_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-783BD)) - 1),5BD)
        return self.daily_cume_return(field=field, periods=783, lag=5, **kwds_args)

    # SIMPLE TRAILING WEEKLY RETURN FACTORS LAGGED 1 WEEK...
    # --------------------------------------------------------
    @RootLib.temp_frame()
    def RET1W_LAG1W(self, field, **kwds_args):
        """Trailing Return (Past 1W) Lagged 1W"""
        # FL:RET1W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-1W)) - 1),1W)
        return self.weekly_cume_return(field=field, periods=1, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET4W_LAG1W(self, field, **kwds_args):
        """Trailing Return (Past 1M=Past 4W) Lagged 1W"""
        # FL:RET4W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-4W)) - 1),1W)
        return self.weekly_cume_return(field=field, periods=4, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET13W_LAG1W(self, field, **kwds_args):
        """Trailing Return (Past 3M=Past 13W) Lagged 1W"""
        # FL:RET13W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-13W)) - 1),1W)
        return self.weekly_cume_return(field=field, periods=13, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET26W_LAG1W(self, field, **kwds_args):
        """Trailing Return (Past 6M=Past 26W) Lagged 1W"""
        # FL:RET26W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-26W)) - 1),1W)
        return self.weekly_cume_return(field=field, periods=26, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET39W_LAG1W(self, field, **kwds_args):
        """Trailing Return (Past 9M=Past 39W) Lagged 1W"""
        # FL:RET39W_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-39WBD)) - 1),1W)
        return self.weekly_cume_return(field=field, periods=39, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET52W_LAG1W(self, field, **kwds_args):
        """Trailing Return (Past 12M=Past 52W) Lagged 1W"""
        # FL:RET52W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-52W)) - 1),1W)
        return self.weekly_cume_return(field=field, periods=52, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET78W_LAG1W(self, field, **kwds_args):
        """Trailing Return (Past 18M=Past 78W) Lagged 1W"""
        # FL:RET78W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-78W)) - 1),1W)
        return self.weekly_cume_return(field=field, periods=78, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET156W_LAG1W(self, field, **kwds_args):
        """Trailing Return (Past 36M=Past 3*261BD=Past 3*52W = Past 78 W) Lagged 1W"""
        # FL:RET156W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-156W)) - 1),1W)
        return self.weekly_cume_return(field=field, periods=156, lag=1, **kwds_args)

    # SIMPLE TRAILING DAILY RETURN FACTORS LAGGED 22 DBAYS...
    # ---------------------------------------------------------
    @RootLib.temp_frame()
    def RET1D_LAG22D(self, field, **kwds_args):
        """Trailing Return (Past 1BD) Lagged 22BD"""
        # FL:RET1D_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-1)) - 1BD),22BD)
        return self.daily_cume_return(field=field, periods=1, lag=22, **kwds_args)

    @RootLib.temp_frame()
    def RET5D_LAG22D(self, field, **kwds_args):
        """Trailing Return (Past 5BD) Lagged 22BD"""
        # FL:RET5D_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-5BD)) - 1),22BD)
        return self.daily_cume_return(field=field, periods=5, lag=22, **kwds_args)

    @RootLib.temp_frame()
    def RET22D_LAG22D(self, field, **kwds_args):
        """Trailing Return (Past 1M=Past 22BD) Lagged 22BD"""
        # FL:RET1M_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-22BD)) - 1),22BD)
        return self.daily_cume_return(field=field, periods=22, lag=22, **kwds_args)

    @RootLib.temp_frame()
    def RET65D_LAG22D(self, field, **kwds_args):
        """Trailing Return (Past 3M=Past 65BD) Lagged 22BD"""
        # FL:RET3M_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-65BD)) - 5),22BD)
        return self.daily_cume_return(field=field, periods=65, lag=22, **kwds_args)

    @RootLib.temp_frame()
    def RET130D_LAG22D(self, field, **kwds_args):
        """Trailing Return (Past 6M=Past 130BD) Lagged 22BD"""
        # FL:RET130D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-130BD)) - 1),22BD)
        return self.daily_cume_return(field=field, periods=130, lag=22, **kwds_args)

    @RootLib.temp_frame()
    def RET196D_LAG22D(self, field, **kwds_args):
        """Trailing Return (Past 9M=Past 196BD) Lagged 22BD"""
        # FL:RET196D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-196BD)) - 1),22BD)
        return self.daily_cume_return(field=field, periods=196, lag=22, **kwds_args)

    @RootLib.temp_frame()
    def RET261D_LAG22D(self, field, **kwds_args):
        """Trailing Return (Past 12M=Past 261BD) Lagged 22BD"""
        # FL:RET261D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-261BD)) - 1),22BD)
        return self.daily_cume_return(field=field, periods=261, lag=22, **kwds_args)

    @RootLib.temp_frame()
    def RET392D_LAG22D(self, field, **kwds_args):
        """Trailing Return (Past 18M=Past 392BD) Lagged 22BD"""
        # FL:RET392D_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-392BD)) - 1),22BD)
        return self.daily_cume_return(field=field, periods=392, lag=22, **kwds_args)

    @RootLib.temp_frame()
    def RET783D_LAG22D(self, field, **kwds_args):
        """Trailing Return (Past 36M=Past 3*261BD=Past 783BD) Lagged 22BD"""
        # FL:RET36M_LAG1D = SHIFT(((CLOSE(T)-CLOSE(T-783BD)) - 1),22BD)
        return self.daily_cume_return(field=field, periods=783, lag=22, **kwds_args)

    # SIMPLE TRAILING WEEKLY RETURN FACTORS LAGGED 4 WEEKS...
    # ---------------------------------------------------------
    @RootLib.temp_frame()
    def RET1W_LAG4W(self, field, **kwds_args):
        """Trailing Return (Past 1W) Lagged 4W"""
        # FL:RET1W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-1W)) - 1),4W)
        return self.weekly_cume_return(field=field, periods=1, lag=4, **kwds_args)

    @RootLib.temp_frame()
    def RET4W_LAG4W(self, field, **kwds_args):
        """Trailing Return (Past 1M=Past 4W) Lagged 4W"""
        # FL:RET4W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-4W)) - 1),4W)
        return self.weekly_cume_return(field=field, periods=4, lag=4, **kwds_args)

    @RootLib.temp_frame()
    def RET13W_LAG4W(self, field, **kwds_args):
        """Trailing Return (Past 3M=Past 13W) Lagged 4W"""
        # FL:RET13W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-13W)) - 1),4W)
        return self.weekly_cume_return(field=field, periods=13, lag=4, **kwds_args)

    @RootLib.temp_frame()
    def RET26W_LAG4W(self, field, **kwds_args):
        """Trailing Return (Past 6M=Past 26W) Lagged 4W"""
        # FL:RET26W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-26W)) - 1),4W)
        return self.weekly_cume_return(field=field, periods=26, lag=4, **kwds_args)

    @RootLib.temp_frame()
    def RET39W_LAG4W(self, field, **kwds_args):
        """Trailing Return (Past 9M=Past 39W) Lagged 4W"""
        # FL:RET39W_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-39WBD)) - 1),4W)
        return self.weekly_cume_return(field=field, periods=39, lag=4, **kwds_args)

    @RootLib.temp_frame()
    def RET52W_LAG4W(self, field, **kwds_args):
        """Trailing Return (Past 12M=Past 52W) Lagged 4W"""
        # FL:RET52W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-52W)) - 1),4W)
        return self.weekly_cume_return(field=field, periods=52, lag=4, **kwds_args)

    @RootLib.temp_frame()
    def RET78W_LAG4W(self, field, **kwds_args):
        """Trailing Return (Past 18M=Past 78W) Lagged 4W"""
        # FL:RET78W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-78W)) - 1),4W)
        return self.weekly_cume_return(field=field, periods=78, lag=4, **kwds_args)

    @RootLib.temp_frame()
    def RET156W_LAG4W(self, field, **kwds_args):
        """Trailing Return (Past 36M=Past 3*261BD=Past 3*52W = Past 78 W) Lagged 4W"""
        # FL:RET156W_LAG1W = SHIFT(((CLOSE(T)/CLOSE(T-156W)) - 1),4W)
        return self.weekly_cume_return(field=field, periods=156, lag=4, **kwds_args)

    # SIMPLE TRAILING MONTHLY RETURN FACTORS LAGGED 1 MONTH...
    # ----------------------------------------------------------
    @RootLib.temp_frame()
    def RET1M_LAG1M(self, field, **kwds_args):
        """Trailing Return (Past 1M=Past 22BD) Lagged 1M = Lagged 1M"""
        # FL:RET1M_LAG1M = SHIFT(((CLOSE(T)/CLOSE(T-1M)) - 1),1M)
        return self.monthly_cume_return(field=field, periods=1, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET3M_LAG1M(self, field, **kwds_args):
        """Trailing Return (Past 3M=Past 65BD) Lagged 1M = Lagged 22BD"""
        # FL:RET3M_LAG1M = SHIFT(((CLOSE(T)/CLOSE(T-3M)) - 1),1M)
        return self.monthly_cume_return(field=field, periods=3, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET6M_LAG1M(self, field, **kwds_args):
        """Trailing Return (Past 6M=Past 130BD) Lagged 1M = Lagged 22BD"""
        # FL:RET6M_LAG1M = SHIFT(((CLOSE(T)/CLOSE(T-6M)) - 1),1M)
        return self.monthly_cume_return(field=field, periods=6, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET9M_LAG1M(self, field, **kwds_args):
        """Trailing Return (Past 9M=Past 196BD) Lagged 1M = Lagged 22BD"""
        # FL:RET9M_LAG1D = SHIFT(((CLOSE(T)/CLOSE(T-9M)) - 1),1M)
        return self.monthly_cume_return(field=field, periods=9, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET12M_LAG1M(self, field, **kwds_args):
        """Trailing Return (Past 12M=Past 261BD) Lagged 1M = Lagged 22BD"""
        # FL:RET12M_LAG1M = SHIFT(((CLOSE(T)/CLOSE(T-12M)) - 1),1M)
        return self.monthly_cume_return(field=field, periods=12, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET18M_LAG1M(self, field, **kwds_args):
        """Trailing Return (Past 18M=Past 392BD) Lagged 1M = Lagged 22BD"""
        # FL:RET18M_LAG1M = SHIFT(((CLOSE(T)/CLOSE(T-18M)) - 1),1M)
        return self.monthly_cume_return(field=field, periods=18, lag=1, **kwds_args)

    @RootLib.temp_frame()
    def RET36M_LAG1M(self, field, **kwds_args):
        """Trailing Return (Past 36M=Past 3*261BD=Past 783BD) Lagged 1M = Lagged 22BD"""
        # FL:RET36M_LAG1M = SHIFT(((CLOSE(T)/CLOSE(T-36M)) - 1),1M)
        return self.monthly_cume_return(field=field, periods=36, lag=1, **kwds_args)

    # RATIOS OF PRICE TO TRAILING HIGH...
    # -------------------------------------
    @RootLib.temp_frame()
    def P2HIGH_5D(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,5BD)"""
        # FL:P2HIGH_5D = CLOSE(T) / MMAX(CLOSE(T),5BD)
        return self.daily_p2high(field=field, periods=5, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_22D(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,22BD)"""
        # FL:P2HIGH_22D = CLOSE(T) / MMAX(CLOSE(T),22BD)
        return self.daily_p2high(field=field, periods=22, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_4W(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,4W)"""
        # FL:P2HIGH_4W = CLOSE(T) / MMAX(CLOSE(T),4W)
        return self.weekly_p2high(field=field, periods=4, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_65D(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,65BD)"""
        # FL:P2HIGH_65D = CLOSE(T) / MMAX(CLOSE(T),65BD)
        return self.daily_p2high(field=field, periods=65, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_13W(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,13W)"""
        # FL:P2HIGH_13W = CLOSE(T) / MMAX(CLOSE(T),13W)
        return self.weekly_p2high(field=field, periods=13, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_3M(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,3M)"""
        # FL:P2HIGH_3M = CLOSE(T) / MMAX(CLOSE(T),3M)
        return self.monthly_p2high(field=field, periods=3, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_130D(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,130BD)"""
        # FL:P2HIGH_130D = CLOSE(T) / MMAX(CLOSE(T),130BD)
        return self.daily_p2high(field=field, periods=130, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_26W(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,26W)"""
        # FL:P2HIGH_126W = CLOSE(T) / MMAX(CLOSE(T),26W)
        return self.weekly_p2high(field=field, periods=26, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_6M(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,6M)"""
        # FL:P2HIGH_6M = CLOSE(T) / MMAX(CLOSE(T),3M)
        return self.monthly_p2high(field=field, periods=6, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_261D(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,261BD)"""
        # FL:P2HIGH_261D = CLOSE(T) / MMAX(CLOSE(T),261BD)
        return self.daily_p2high(field=field, periods=261, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_52W(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,52W)"""
        # FL:P2HIGH_52W = CLOSE(T) / MMAX(CLOSE(T),52W)
        return self.weekly_p2high(field=field, periods=52, **kwds_args)

    @RootLib.temp_frame()
    def P2HIGH_12M(self, field, **kwds_args):
        """Ratio: CLOSE / MHIGH(CLOSE,12M)"""
        # FL:P2HIGH_12M = CLOSE(T) / MMAX(CLOSE(T),12M)
        return self.monthly_p2high(field=field, periods=12, **kwds_args)

    # RATIOS OF PRICE TO TRAILING LOW...
    # ------------------------------------
    @RootLib.temp_frame()
    def P2LOW_5D(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,5BD)"""
        # FL:P2LOW_5D = CLOSE(T) / MMAX(CLOSE(T),5BD)
        return self.daily_p2low(field=field, periods=5, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_22D(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,22BD)"""
        # FL:P2LOW_22D = CLOSE(T) / MMAX(CLOSE(T),22BD)
        return self.daily_p2low(field=field, periods=22, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_4W(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,4W)"""
        # FL:P2LOW_4W = CLOSE(T) / MMAX(CLOSE(T),4W)
        return self.weekly_p2low(field=field, periods=4, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_65D(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,65BD)"""
        # FL:P2LOW_65D = CLOSE(T) / MMAX(CLOSE(T),65BD)
        return self.daily_p2low(field=field, periods=65, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_13W(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,13W)"""
        # FL:P2LOW_13W = CLOSE(T) / MMAX(CLOSE(T),13W)
        return self.weekly_p2low(field=field, periods=13, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_3M(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,3M)"""
        # FL:P2LOW_3M = CLOSE(T) / MMAX(CLOSE(T),3M)
        return self.monthly_p2low(field=field, periods=3, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_130D(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,130BD)"""
        # FL:P2LOW_130D = CLOSE(T) / MMAX(CLOSE(T),130BD)
        return self.daily_p2low(field=field, periods=130, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_26W(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,26W)"""
        # FL:P2LOW_126W = CLOSE(T) / MMAX(CLOSE(T),26W)
        return self.weekly_p2low(field=field, periods=26, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_6M(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,6M)"""
        # FL:P2LOW_6M = CLOSE(T) / MMAX(CLOSE(T),3M)
        return self.monthly_p2low(field=field, periods=6, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_261D(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,261BD)"""
        # FL:P2LOW_261D = CLOSE(T) / MMAX(CLOSE(T),261BD)
        return self.daily_p2low(field=field, periods=261, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_52W(self, field, **kwds_args):
        """Ratio: CLOSE / MLOW(CLOSE,52W)"""
        # FL:P2LOW_52W = CLOSE(T) / MMAX(CLOSE(T),52W)
        return self.weekly_p2low(field=field, periods=52, **kwds_args)

    @RootLib.temp_frame()
    def P2LOW_12M(self, field, **kwds_args):
        """Ratio: CLOSE / MLOWCLOSE,12M)"""
        # FL:P2LOW_12M = CLOSE(T) / MMAX(CLOSE(T),12M)
        return self.monthly_p2low(field=field, periods=12, **kwds_args)

    # PRICE MAVE RATIOS & OSCILLATORS...
    # -----------------------------------------
    @RootLib.temp_frame()
    def PRICE_MAVE_RATIO_75D_180D(self, field, **kwds_args):
        """Ratio: MMEAN(CLOSE(T),75BD) /  MMEAN(CLOSE(T),180DB)"""
        # FL:PRICE_MAVE_RATIO_75D_180D = MMEAN(CLOSE,75BD) / MMEAN(CLOSE,180BD)
        return self.daily_price_mave_ratio(
            field=field, short_periods=75, long_periods=180, **kwds_args
        )

    @RootLib.temp_frame()
    def PRICE_MAVE_RATIO_15W_36W(self, field, **kwds_args):
        """Ratio: MMEAN(CLOSE(T),15W) /  MMEAN(CLOSE(T),36W)"""
        # FL:PRICE_MAVE_RATIO_15W_36W = MMEAN(CLOSE,15W) / MMEAN(CLOSE,36W)
        return self.weekly_price_mave_ratio(
            field=field, short_periods=15, long_periods=36, **kwds_args
        )

    @RootLib.temp_frame()
    def PRICE_MAVE_RATIO_3M_8M(self, field, **kwds_args):
        """Ratio: MMEAN(CLOSE(T),3M) /  MMEAN(CLOSE(T),8M)"""
        # FL:PRICE_MAVE_RATIO_3M_8M = MMEAN(CLOSE,3M) / MMEAN(CLOSE,8M)
        return self.monthly_price_mave_ratio(
            field=field, short_periods=3, long_periods=9, **kwds_args
        )

    @RootLib.temp_frame()
    def PRICE_MAVE_RATIO_150D_375D(self, field, **kwds_args):
        """Ratio: MMEAN(CLOSE(T),150BD) /  MMEAN(CLOSE(T),375DB)"""
        # FL:PRICE_MAVE_RATIO_150D_375D = MMEAN(CLOSE,150BD) / MMEAN(CLOSE,375BD)
        return self.daily_price_mave_ratio(
            field=field, short_periods=150, long_periods=375, **kwds_args
        )

    @RootLib.temp_frame()
    def PRICE_MAVE_RATIO_30W_75W(self, field, **kwds_args):
        """Ratio: MMEAN(CLOSE(T),30W) /  MMEAN(CLOSE(T),75W)"""
        # FL:PRICE_MAVE_RATIO_30W_75W = MMEAN(CLOSE,30W) / MMEAN(CLOSE,75W)
        return self.weekly_price_mave_ratio(
            field=field, short_periods=30, long_periods=75, **kwds_args
        )

    @RootLib.temp_frame()
    def PRICE_MAVE_RATIO_7M_18M(self, field, **kwds_args):
        """Ratio: MMEAN(CLOSE(T),7M) /  MMEAN(CLOSE(T),18M)"""
        # FL:PRICE_MAVE_RATIO_7M_18M = MMEAN(CLOSE,7M) / MMEAN(CLOSE,18M)
        return self.monthly_price_mave_ratio(
            field=field, short_periods=7, long_periods=18, **kwds_args
        )

    @RootLib.temp_frame()
    def REL_STOCH_OSC_39D(self, field, **kwds_args):
        """RELATIVE STOCHASTIC OSCILLATOR (39D) = RULE ACCORDING STOCH_FAST & STOCH_SLOW...
        REL_STOCH_OSC_39D = +1, IF STOCH_FAST>75 & STOCH_SLOW>75 & STOCH_FAST<STOCH_SLOW (TRENDING UP & OVERSOLD)
        REL_STOCH_OSC_39D = -1, IF STOCH_FAST<25 & STOCH_SLOW<25 & STOCH_FAST>STOCH_SLOW (TRENDING DOWN & OVERBOUGHT)
        REL_STOCH_OSC_39D =  0, OTHERWISE
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        stoch_osc = self._stoch_osc(
            field=field,
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=39,
            rel_flag=True,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            stoch_osc = stoch_osc.asfreq(freq, keyspace=dates_keyspace)
        return stoch_osc

    @RootLib.temp_frame()
    def REL_STOCH_OSC_8W(self, field, **kwds_args):
        """RELATIVE STOCHASTIC OSCILLATOR (39BD=8W) = RULE ACCORDING STOCH_FAST & STOCH_SLOW...
        REL_STOCH_OSC_39D = +1, IF STOCH_FAST>75 & STOCH_SLOW>75 & STOCH_FAST<STOCH_SLOW (TRENDING UP & OVERSOLD)
        REL_STOCH_OSC_39D = -1, IF STOCH_FAST<25 & STOCH_SLOW<25 & STOCH_FAST>STOCH_SLOW (TRENDING DOWN & OVERBOUGHT)
        REL_STOCH_OSC_39D =  0, OTHERWISE
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        stoch_osc = self._stoch_osc(
            field=field,
            prc_lib=prc_lib,
            freq=weekly_freq,
            dates_keyspace=dates_keyspace,
            periods=8,
            rel_flag=True,
            **kwds_args,
        )
        if freq != weekly_freq:
            stoch_osc = stoch_osc.asfreq(freq, keyspace=dates_keyspace)
        return stoch_osc

    @RootLib.temp_frame()
    def REL_STOCH_OSC_304D(self, field, **kwds_args):
        """RELATIVE STOCHASTIC OSCILLATOR (304BD=61W=14M) = RULE ACCORDING STOCH_FAST & STOCH_SLOW...
        REL_STOCH_OSC_304D = +1, IF STOCH_FAST>75 & STOCH_SLOW>75 & STOCH_FAST<STOCH_SLOW (TRENDING UP & OVERSOLD)
        REL_STOCH_OSC_304D = -1, IF STOCH_FAST<25 & STOCH_SLOW<25 & STOCH_FAST>STOCH_SLOW (TRENDING DOWN & OVERBOUGHT)
        REL_STOCH_OSC_304D =  0, OTHERWISE
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        stoch_osc = self._stoch_osc(
            field=field,
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=304,
            rel_flag=True,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            stoch_osc = stoch_osc.asfreq(freq, keyspace=dates_keyspace)
        return stoch_osc

    @RootLib.temp_frame()
    def REL_STOCH_OSC_61W(self, field, **kwds_args):
        """RELATIVE STOCHASTIC OSCILLATOR (304BD=61W=14M) = RULE ACCORDING STOCH_FAST & STOCH_SLOW...
        REL_STOCH_OSC_14W = +1, IF STOCH_FAST>75 & STOCH_SLOW>75 & STOCH_FAST<STOCH_SLOW (TRENDING UP & OVERSOLD)
        REL_STOCH_OSC_14W = -1, IF STOCH_FAST<25 & STOCH_SLOW<25 & STOCH_FAST>STOCH_SLOW (TRENDING DOWN & OVERBOUGHT)
        REL_STOCH_OSC_14W =  0, OTHERWISE
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        stoch_osc = self._stoch_osc(
            field=field,
            prc_lib=prc_lib,
            freq=weekly_freq,
            dates_keyspace=dates_keyspace,
            periods=61,
            rel_flag=True,
            **kwds_args,
        )
        if freq != weekly_freq:
            stoch_osc = stoch_osc.asfreq(freq, keyspace=dates_keyspace)
        return stoch_osc

    @RootLib.temp_frame()
    def REL_STOCH_OSC_14M(self, field, **kwds_args):
        """RELATIVE STOCHASTIC OSCILLATOR (304BD=61W=14M) = RULE ACCORDING STOCH_FAST & STOCH_SLOW...
        REL_STOCH_OSC_4M = +1, IF STOCH_FAST>75 & STOCH_SLOW>75 & STOCH_FAST<STOCH_SLOW (TRENDING UP & OVERSOLD)
        REL_STOCH_OSC_4M = -1, IF STOCH_FAST<25 & STOCH_SLOW<25 & STOCH_FAST>STOCH_SLOW (TRENDING DOWN & OVERBOUGHT)
        REL_STOCH_OSC_4M =  0, OTHERWISE
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        stoch_osc = self._stoch_osc(
            field=field,
            prc_lib=prc_lib,
            freq="CEOM",
            dates_keyspace=dates_keyspace,
            periods=14,
            rel_flag=True,
            **kwds_args,
        )
        if freq != "CEOM":
            stoch_osc = stoch_osc.asfreq(freq, keyspace=dates_keyspace)
        return stoch_osc

    def _stoch_osc(
        self, field, prc_lib, freq, dates_keyspace, periods, rel_flag, **kwds_args
    ):
        # FL:REL_STOCH_OSC_39D = DISCRETE RULES ON STOCH_FAST & STOCH_SLOW

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        if rel_flag:
            index_price_field = self.get_property(
                "index_price_field", field, grace=False, resolve_templates=True
            )
            index_price = RootLib()[index_price_field]
            if index_price is None:
                raise Exception(f"Could not procure market_index:{index_price_field}")
            elif index_price.is_empty:
                raise Exception(f"Empty market_index:{index_price_field}")
            elif dates_keyspace not in index_price.keyspaces:
                raise Exception(
                    f"index_price.keyspaces does not contain {dates_keyspace}"
                )
            elif dates_keyspace not in close.keyspaces:
                raise Exception(f"close.keyspaces does not contain {dates_keyspace}")

            # Massage index_price to align (freq & dates) with close
            index_price = index_price.fill1d(
                dates_keyspace, tfill_method="pad", tfill_max=5
            ).reindex1d(index=close, keyspace=dates_keyspace)
            rel_close = close / index_price
        else:
            rel_close = close

        rel_close_mmin = rel_close.mmin1d(
            periods=periods,
            keyspace=dates_keyspace,
            pct_required=0.5,
            ignore_missing=True,
        )
        rel_close_mmax = rel_close.mmax1d(
            periods=periods,
            keyspace=dates_keyspace,
            pct_required=0.5,
            ignore_missing=True,
        )
        rel_stoch_range = 100.0 * (
            (rel_close - rel_close_mmin) / (rel_close_mmax - rel_close_mmin)
        )

        rel_stoch_fast = rel_stoch_range.decay_filter1d(
            decay_factor=0.67, max_missing_counter=10, keyspace=dates_keyspace
        )

        rel_stoch_slow = rel_stoch_fast.decay_filter1d(
            decay_factor=0.67, max_missing_counter=10, keyspace=dates_keyspace
        )

        # Convert rel_stoch_fast & rel_stoch_slow into discrete signal: +1,0,-1
        # -----------------------------------------------------------------------
        trending_up_and_oversold = (
            (rel_stoch_fast > 75)
            & (rel_stoch_slow > 75)
            & (rel_stoch_fast < rel_stoch_slow)
        )
        trending_down_and_overbought = (
            (rel_stoch_fast < 25)
            & (rel_stoch_slow < 25)
            & (rel_stoch_fast > rel_stoch_slow)
        )
        rel_stoch_osc = rel_stoch_fast.replace_non_missings(new_value=0.0)
        rel_stoch_osc[rel_stoch_osc.where_not_missing()] = 0
        rel_stoch_osc[trending_up_and_oversold] = 1
        rel_stoch_osc[trending_down_and_overbought] = -1
        return rel_stoch_osc

    @RootLib.temp_frame()
    def LOTTERY_22D(self, field, **kwds_args):
        """Lottery Factor (Past 22 BDays) = Max Return (Past 22 BDays)
        Prior:NEGATIVE"""
        # FL:LOTTERY_22D = MMAX(TRETS,22)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        daily_returns = self.get_calendarized_field(
            field_prefix="TRI", freq="WEEKDAY", lib=prc_lib
        )
        max_return_22d = daily_returns.mmax1d(
            periods=22, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != "WEEKDAY":
            max_return_22d = max_return_22d.asfreq(freq, keyspace=dates_keyspace)
        return max_return_22d

    def _WILLIAMS_R(self, prc_lib, freq, dates_keyspace, periods, **kwds_args):
        """Williams %R = -100. * (HIGHEST_HIGH_<periods>D - CLOSE) / (HIGHEST_HIGH_<periods>D - LOWEST_LOW_<periods>D)
        Prior:NEGATIVE, Range:[-100 (OVERSOLD/BULLISH),0(OVERBOUGHT/BEARISH)]"""

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        high = self.get_calendarized_field(
            field_prefix="HIGH",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        low = self.get_calendarized_field(
            field_prefix="LOW",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        highest_high = high.mmax1d(
            periods=periods,
            keyspace=dates_keyspace,
            pct_required=0.5,
            ignore_missing=True,
        )
        lowest_low = low.mmin1d(
            periods=periods,
            keyspace=dates_keyspace,
            pct_required=0.5,
            ignore_missing=True,
        )
        williams_r = -100.0 * (highest_high - close) / (highest_high - lowest_low)
        return williams_r

    @RootLib.temp_frame()
    def WILLIAMS_R_5D(self, field, **kwds_args):
        """Williams %R (Past 5 BDays) = -100. * (HIGHEST_HIGH_5D - CLOSE) / (HIGHEST_HIGH_5D - LOWEST_LOW_5D)
        Prior:NEGATIVE, Range:[-100 (OVERSOLD/BULLISH),0(OVERBOUGHT/BEARISH)]"""
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        williams_r = self._WILLIAMS_R(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=5,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            williams_r = williams_r.asfreq(freq=freq, keyspace=dates_keyspace)

        return williams_r

    @RootLib.temp_frame()
    def WILLIAMS_R_14D(self, field, **kwds_args):
        """Williams %R (Past 14 BDays) = -100. * (HIGHEST_HIGH_14D - CLOSE) / (HIGHEST_HIGH_14D - LOWEST_LOW_14D)
        Prior:NEGATIVE, Range:[-100 (OVERSOLD/BULLISH),0(OVERBOUGHT/BEARISH)]"""
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        williams_r = self._WILLIAMS_R(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=14,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            williams_r = williams_r.asfreq(freq=freq, keyspace=dates_keyspace)
        return williams_r

    @RootLib.temp_frame()
    def WILLIAMS_R_22D(self, field, **kwds_args):
        """Williams %R (Past 22 BDays) = -100. * (HIGHEST_HIGH_22D - CLOSE) / (HIGHEST_HIGH_22D - LOWEST_LOW_22D)
        Prior:NEGATIVE, Range:[-100 (OVERSOLD/BULLISH),0(OVERBOUGHT/BEARISH)]"""
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        williams_r = self._WILLIAMS_R(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=22,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            williams_r = williams_r.asfreq(freq=freq, keyspace=dates_keyspace)
        return williams_r

    @RootLib.temp_frame()
    def WILLIAMS_R_65D(self, field, **kwds_args):
        """Williams %R (Past 65 BDays) = -100. * (HIGHEST_HIGH_65D - CLOSE) / (HIGHEST_HIGH_65D - LOWEST_LOW_65D)
        Prior:NEGATIVE, Range:[-100 (OVERSOLD/BULLISH),0(OVERBOUGHT/BEARISH)]"""
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )
        williams_r = self._WILLIAMS_R(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=65,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            williams_r = williams_r.asfreq(freq=freq, keyspace=dates_keyspace)
        return williams_r

    def _WILLIAMS_R_REL(
        self, prc_lib, freq, dates_keyspace, periods, rel_periods, **kwds_args
    ):
        """Williams%R(periods) / MMEAN(Williams%R(periods), rel_periods)
        NOTE: Due to both numerator & denominator terms being NEGATIVE,
        the prediction direction if this normalized Williams indicator (Williams Ratio) changes from that of the stand alone Williams
        Williams Ratio Prior:POSITIVE (Normalized by a Negative Number)
        Prior:POSITIVE; Where: Williams%R(nD) = -100. * (HIGHEST_HIGH_nD - CLOSE) / (HIGHEST_HIGH_nD - LOWEST_LOW_nD)
        """
        williams_r = self._WILLIAMS_R(
            prc_lib=prc_lib,
            freq=freq,
            dates_keyspace=dates_keyspace,
            periods=periods,
            **kwds_args,
        )
        williams_r_mave = williams_r.mmean1d(
            periods=rel_periods,
            keyspace=dates_keyspace,
            pct_required=0.5,
            ignore_missing=True,
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        williams_rel = williams_r / williams_r_mave
        return williams_rel

    @RootLib.temp_frame()
    def WILLIAMS_R_5D22D(self, field, **kwds_args):
        """Williams%R(5D) / MMEAN(Williams%R(5D), 22D)
        NOTE: Due to both numerator & denominator terms being negative,
        the prediction direction if this normalized Williams indicator (Williams Ratio) changes from that of the stand alone Williams
        Williams Ratio Prior:POSITIVE (Normalized by a Negative Number)
        Where: Williams%R(5D) = -100. * (HIGHEST_HIGH_5D - CLOSE) / (HIGHEST_HIGH_5D - LOWEST_LOW_5D)
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        wiliams_r_rel = self._WILLIAMS_R_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=5,
            rel_periods=22,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            wiliams_r_rel = wiliams_r_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return wiliams_r_rel

    @RootLib.temp_frame()
    def WILLIAMS_R_5D65D(self, field, **kwds_args):
        """Williams%R(5D) / MMEAN(Williams%R(5D), 65D)
        Prior:NEGATIVE; Where: Williams%R(5D) = -100. * (HIGHEST_HIGH_5D - CLOSE) / (HIGHEST_HIGH_5D - LOWEST_LOW_5D)
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        wiliams_r_rel = self._WILLIAMS_R_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=5,
            rel_periods=65,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            wiliams_r_rel = wiliams_r_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return wiliams_r_rel

    @RootLib.temp_frame()
    def WILLIAMS_R_5D261D(self, field, **kwds_args):
        """Williams%R(5D) / MMEAN(Williams%R(5D), 261D)
        Prior:NEGATIVE; Where: Williams%R(5D) = -100. * (HIGHEST_HIGH_5D - CLOSE) / (HIGHEST_HIGH_5D - LOWEST_LOW_5D)
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        wiliams_r_rel = self._WILLIAMS_R_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=5,
            rel_periods=261,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            wiliams_r_rel = wiliams_r_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return wiliams_r_rel

    @RootLib.temp_frame()
    def WILLIAMS_R_14D22D(self, field, **kwds_args):
        """Williams%R(14D) / MMEAN(Williams%R(14D), 22D)
        NOTE: Due to both numerator & denominator terms being NEGATIVE,
        the prediction direction if this normalized Williams indicator (Williams Ratio) changes from that of the stand alone Williams
        Williams Ratio Prior:POSITIVE (Normalized by a Negative Number)
        Prior:POSITIVE; Where: Williams%R(14D) = -100. * (HIGHEST_HIGH_14D - CLOSE) / (HIGHEST_HIGH_14D - LOWEST_LOW_14D)
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        wiliams_r_rel = self._WILLIAMS_R_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=14,
            rel_periods=22,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            wiliams_r_rel = wiliams_r_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return wiliams_r_rel

    @RootLib.temp_frame()
    def WILLIAMS_R_14D65D(self, field, **kwds_args):
        """Williams%R(14D) / MMEAN(Williams%R(14D), 65D)
        NOTE: Due to both numerator & denominator terms being NEGATIVE,
        the prediction direction if this normalized Williams indicator (Williams Ratio) changes from that of the stand alone Williams
        Williams Ratio Prior:POSITIVE (Normalized by a Negative Number)
        Prior:POSITIVE; Where: Williams%R(14D) = -100. * (HIGHEST_HIGH_14D - CLOSE) / (HIGHEST_HIGH_14D - LOWEST_LOW_14D)
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        wiliams_r_rel = self._WILLIAMS_R_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=14,
            rel_periods=65,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            wiliams_r_rel = wiliams_r_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return wiliams_r_rel

    @RootLib.temp_frame()
    def WILLIAMS_R_14D261D(self, field, **kwds_args):
        """Williams%R(14D) / MMEAN(Williams%R(14D), 261D)
        NOTE: Due to both numerator & denominator terms being NEGATIVE,
        the prediction direction if this normalized Williams indicator (Williams Ratio) changes from that of the stand alone Williams
        Williams Ratio Prior:POSITIVE (Normalized by a Negative Number)
        Prior:POSITIVE; Where: Williams%R(14D) = -100. * (HIGHEST_HIGH_14D - CLOSE) / (HIGHEST_HIGH_14D - LOWEST_LOW_14D)
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        wiliams_r_rel = self._WILLIAMS_R_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=14,
            rel_periods=261,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            wiliams_r_rel = wiliams_r_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return wiliams_r_rel

    @RootLib.temp_frame()
    def WILLIAMS_R_22D65D(self, field, **kwds_args):
        """Williams%R(22D) / MMEAN(Williams%R(22D), 65D)
        NOTE: Due to both numerator & denominator terms being NEGATIVE,
        the prediction direction if this normalized Williams indicator (Williams Ratio) changes from that of the stand alone Williams
        Williams Ratio Prior:POSITIVE (Normalized by a Negative Number)
        Prior:POSITIVE; Where: Williams%R(22D) = -100. * (HIGHEST_HIGH_22D - CLOSE) / (HIGHEST_HIGH_22D - LOWEST_LOW_22D)
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        wiliams_r_rel = self._WILLIAMS_R_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=22,
            rel_periods=65,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            wiliams_r_rel = wiliams_r_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return wiliams_r_rel

    @RootLib.temp_frame()
    def WILLIAMS_R_22D261D(self, field, **kwds_args):
        """Williams%R(22D) / MMEAN(Williams%R(22D), 261D)
        NOTE: Due to both numerator & denominator terms being NEGATIVE,
        the prediction direction if this normalized Williams indicator (Williams Ratio) changes from that of the stand alone Williams
        Williams Ratio Prior:POSITIVE (Normalized by a Negative Number)
        Prior:POSITIVE; Where: Williams%R(22D) = -100. * (HIGHEST_HIGH_22D - CLOSE) / (HIGHEST_HIGH_22D - LOWEST_LOW_22D)
        """
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        wiliams_r_rel = self._WILLIAMS_R_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=22,
            rel_periods=261,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            wiliams_r_rel = wiliams_r_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return wiliams_r_rel

    def _CLV_BASE(self, prc_lib, freq, **kwds_args):
        """Williams %R = -100. * (HIGHEST_HIGH_<periods>D - CLOSE) / (HIGHEST_HIGH_<periods>D - LOWEST_LOW_<periods>D)
        Prior:NEGATIVE, Range:[-100 (OVERSOLD/BULLISH),0(OVERBOUGHT/BEARISH)]"""

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        high = self.get_calendarized_field(
            field_prefix="HIGH",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        low = self.get_calendarized_field(
            field_prefix="LOW",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        clv_base = ((close - low) - (high - close)) / (high - low)
        return clv_base

    def _CLV_REL(
        self,
        prc_lib,
        freq,
        dates_keyspace,
        periods,
        pct_required=0.5,
        ignore_missing=True,
        **kwds_args,
    ):
        """Williams %R = -100. * (HIGHEST_HIGH_<periods>D - CLOSE) / (HIGHEST_HIGH_<periods>D - LOWEST_LOW_<periods>D)
        Prior:NEGATIVE, Range:[-100 (OVERSOLD/BULLISH),0(OVERBOUGHT/BEARISH)]"""
        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq=freq)
        clv_base_mave = clv_base.mmean1d(
            periods,
            keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        return clv_base / clv_base_mave

    @RootLib.temp_frame()
    def CLV_22D(self, field, **kwds_args):
        """CLV_22D = CLV_BASE / MMEAN(CLV_BASE, 22D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_22D = CLV_BASE / MAVE(CLV_BASE,22D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        result = self._CLV_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=22,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def CLV_65D(self, field, **kwds_args):
        """CLV_65D = CLV_BASE / MMEAN(CLV_BASE, 65D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_65D = CLV_BASE / MAVE(CLV_BASE,65D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        result = self._CLV_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            periods=65,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def CLV_DIFF22D(self, field, **kwds_args):
        """CLV_DIFF22D = MDIFF(CLV_BASE, 22D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_DIFF22D = MDIFF(CLV_BASE,22D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq="WEEKDAY", **kwds_args)
        result = clv_base.mdiff1d(22, keyspace=dates_keyspace)
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def CLV_DIFF65D(self, field, **kwds_args):
        """CLV_DIFF22D = MDIFF(CLV_BASE, 65D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_DIFF22D = MDIFF(CLV_BASE,65D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq="WEEKDAY", **kwds_args)
        result = clv_base.mdiff1d(65, keyspace=dates_keyspace)
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def CLV_AVE10D(self, field, **kwds_args):
        """CLV_AVE22D = MMEAN(CLV_BASE, 10D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_10D = MAVE(CLV_BASE,10D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq="WEEKDAY", **kwds_args)
        result = clv_base.mmean1d(10, keyspace=dates_keyspace, ignore_missing=False)
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def CLV_AVE22D(self, field, **kwds_args):
        """CLV_AVE22D = MMEAN(CLV_BASE, 22D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_22D = MAVE(CLV_BASE,22D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq="WEEKDAY", **kwds_args)
        result = clv_base.mmean1d(
            22, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=False
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def CLV_AVE65D(self, field, **kwds_args):
        """CLV_AVE65D = MMEAN(CLV_BASE, 65D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_65D = MAVE(CLV_BASE,65D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq="WEEKDAY", **kwds_args)
        result = clv_base.mmean1d(
            65, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=False
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def CLV_AVE130D(self, field, **kwds_args):
        """CLV_AVE65D = MMEAN(CLV_BASE, 130D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_AVE130D = MAVE(CLV_BASE,130D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq="WEEKDAY", **kwds_args)
        result = clv_base.mmean1d(
            130, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=False
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def CLV_AVE130D_LAG5D(self, field, **kwds_args):
        """CLV_AVE65D = LAG(MMEAN(CLV_BASE, 130D),5D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_AVE130D_LAG5D = LAG(MAVE(CLV_BASE,130D),5D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq="WEEKDAY", **kwds_args)
        result = clv_base.mmean1d(
            130, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=False
        ).shift1d(periods=5, keyspace=dates_keyspace)
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def CLV_AVE130D_LAG10D(self, field, **kwds_args):
        """CLV_AVE130D_LAG10D = LAG(MMEAN(CLV_BASE, 130D),10D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_AVE130D_LAG5D = LAG(MAVE(CLV_BASE,130D),10D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq="WEEKDAY", **kwds_args)
        result = clv_base.mmean1d(
            130, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=False
        ).shift1d(periods=10, keyspace=dates_keyspace)
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def CLV_AVE130D_LAG22D(self, field, **kwds_args):
        """CLV_AVE130D_LAG22D = LAG(MMEAN(CLV_BASE, 130D),22D)
        Where: CLV_BASE = CLOSE LOCATION VALUE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CLV_AVE130D_LAG22D = LAG(MAVE(CLV_BASE,130D),22D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq="WEEKDAY", **kwds_args)
        result = clv_base.mmean1d(
            130, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=False
        ).shift1d(periods=22, keyspace=dates_keyspace)
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    def _ACCUM2DSTRB(
        self,
        prc_lib,
        freq,
        periods,
        dates_keyspace,
        pct_required=0.5,
        ignore_missing=True,
        **kwds_args,
    ):
        """_ACCUM2DSTRB (aka CUMULATIVE MONEY FLOW VOLUME) = MSUM(CLV_BASE * VOLUME, #PERIODS)
        WHERE: CLV_BASE = (((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW))
        Prior:HIGH LEVEL = BULLISH"""
        clv_base = self._CLV_BASE(prc_lib=prc_lib, freq=freq)
        volume = self.get_calendarized_field(
            field_prefix="VOLUME", freq=freq, lib=prc_lib
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        ad = clv_base * volume
        ad_msum = ad.msum1d(
            periods=periods,
            keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
        )
        return ad_msum

    def _ACCUM2DSTRB_REL(
        self,
        prc_lib,
        freq,
        periods,
        rel_periods,
        dates_keyspace,
        pct_required=0.5,
        ignore_missing=True,
        **kwds_args,
    ):
        ad_msum = self._ACCUM2DSTRB(
            prc_lib=prc_lib,
            freq=freq,
            periods=periods,
            dates_keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
            **kwds_args,
        )
        ad_msum_mave = ad_msum.mmean1d(
            rel_periods,
            keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
        )
        ad_msum_mstd = ad_msum.mstd1d(
            rel_periods,
            keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        ad_rel = (ad_msum - ad_msum_mave) / ad_msum_mstd
        return ad_rel

    @RootLib.temp_frame()
    def ACCUM2DSTRB_5D65D(self, field, **kwds_args):
        """ACCUM2DSTRB_5D22D = MSUM(ACCUM2DSTRB_BASE,5D) / MMEAN(MSUM(ACCUM2DSTRB_BASE,5D), 65D)
        WHERE: ACCUM2DSTRB_BASE = [CLV_BASE * VOLUME] = [(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:ACCUM2DSTRB_5D65D = MSUM(ACCUM2DSTRB_BASE,5D) / MMEAN(MSUM(ACCUM2DSTRB_BASE,5D), 65D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        ad_rel = self._ACCUM2DSTRB_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=5,
            rel_periods=65,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            ad_rel = ad_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return ad_rel

    @RootLib.temp_frame()
    def ACCUM2DSTRB_22D261D(self, field, **kwds_args):
        """ACCUM2DSTRB_22D261D = MSUM(ACCUM2DSTRB_BASE,22D) / MMEAN(MSUM(ACCUM2DSTRB_BASE,22D), 261D)
        WHERE: ACCUM2DSTRB_BASE = [CLV_BASE * VOLUME] = [(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:ACCUM2DSTRB_22D261D = MSUM(ACCUM2DSTRB_BASE,22D) / MMEAN(MSUM(ACCUM2DSTRB_BASE,22D), 261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        ad_rel = self._ACCUM2DSTRB_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=22,
            rel_periods=261,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            ad_rel = ad_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return ad_rel

    @RootLib.temp_frame()
    def ACCUM2DSTRB_65D261D(self, field, **kwds_args):
        """ACCUM2DSTRB_65D261D = MSUM(ACCUM2DSTRB_BASE,65D) / MMEAN(MSUM(ACCUM2DSTRB_BASE,65D), 261D)
        WHERE: ACCUM2DSTRB_BASE = [CLV_BASE * VOLUME] = [(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:ACCUM2DSTRB_65D261D = MSUM(ACCUM2DSTRB_BASE,65D) / MMEAN(MSUM(ACCUM2DSTRB_BASE,65D), 261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        ad_rel = self._ACCUM2DSTRB_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=65,
            rel_periods=261,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            ad_rel = ad_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return ad_rel

    def _CMF(
        self,
        prc_lib,
        freq,
        periods,
        dates_keyspace,
        pct_required=0.5,
        ignore_missing=True,
        **kwds_args,
    ):
        ad_msum = self._ACCUM2DSTRB(
            prc_lib=prc_lib,
            freq=freq,
            periods=periods,
            dates_keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
            **kwds_args,
        )

        volume = self.get_calendarized_field(
            field_prefix="VOLUME", freq=freq, lib=prc_lib
        )
        volume_mave = volume.mmean1d(
            periods,
            keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
        )  # <-- VOLUME is provided in Shares (NOT Millions of Shares)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        cmf = ad_msum / volume_mave
        return cmf

    def _CMF_REL(
        self,
        prc_lib,
        freq,
        periods,
        rel_periods,
        dates_keyspace,
        pct_required=0.5,
        ignore_missing=True,
        **kwds_args,
    ):
        cmf_msum = self._CMF(
            prc_lib=prc_lib,
            freq=freq,
            periods=periods,
            dates_keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
            **kwds_args,
        )

        cmf_msum_mave = cmf_msum.mmean1d(
            rel_periods,
            keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
        )
        cmf_msum_mstd = cmf_msum.mstd1d(
            rel_periods,
            keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
        )
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        cmf_rel = (cmf_msum - cmf_msum_mave) / cmf_msum_mstd
        return cmf_rel

    def _CMF_DIFF(
        self,
        prc_lib,
        freq,
        periods,
        rel_periods,
        dates_keyspace,
        pct_required=0.5,
        ignore_missing=True,
        **kwds_args,
    ):
        cmf_msum = self._CMF(
            prc_lib=prc_lib,
            freq=freq,
            periods=periods,
            dates_keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
            **kwds_args,
        )

        cmf_msum_diff = cmf_msum.mdiff1d(
            rel_periods,
            keyspace=dates_keyspace,
        )
        return cmf_msum_diff

    @RootLib.temp_frame()
    def CMF_5D(self, field, **kwds_args):
        """CMF_5D = CHAIKIN'S MONEY FLOW (5D) = [MSUM(ACCUM2DSTRB_BASE,5D) / MSUM(VOLUME,5D)]
        WHERE: ACCUM2DSTRB_BASE = [CLV_BASE * VOLUME] = [(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_5D = MMEAN(ACCUM2DSTRB_BASE, 5D) / MMEAN(VOLUME, 5D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf = self._CMF(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=5,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            cmf = cmf.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf

    @RootLib.temp_frame()
    def CMF_22D(self, field, **kwds_args):
        """CMF_22D = CHAIKIN'S MONEY FLOW (22D) = [MSUM(ACCUM2DSTRB_BASE,22D) / MSUM(VOLUME,22D)]
        WHERE: ACCUM2DSTRB_BASE = [CLV_BASE * VOLUME] = [(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_22D = MMEAN(ACCUM2DSTRB_BASE, 22D) / MMEAN(VOLUME, 22D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf = self._CMF(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=22,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            cmf = cmf.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf

    @RootLib.temp_frame()
    def CMF_65D(self, field, **kwds_args):
        """CMF_65D = CHAIKIN'S MONEY FLOW (65D) = [MSUM(ACCUM2DSTRB_BASE,65D) / MSUM(VOLUME,65D)]
        WHERE: ACCUM2DSTRB_BASE = [CLV_BASE * VOLUME] = [(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_65D = MMEAN(ACCUM2DSTRB_BASE, 65D) / MMEAN(VOLUME, 65D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf = self._CMF(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=65,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            cmf = cmf.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf

    @RootLib.temp_frame()
    def CMF_130D(self, field, **kwds_args):
        """CMF_130D = CHAIKIN'S MONEY FLOW (130D) = [MSUM(ACCUM2DSTRB_BASE,130D) / MSUM(VOLUME,130D)]
        WHERE: ACCUM2DSTRB_BASE = [CLV_BASE * VOLUME] = [(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_130D = MMEAN(ACCUM2DSTRB_BASE, 130D) / MMEAN(VOLUME, 130D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf = self._CMF(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=130,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            cmf = cmf.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf

    @RootLib.temp_frame()
    def CMF_130D_LAG5D(self, field, **kwds_args):
        """CMF_130D_LAG5D = CHAIKIN'S MONEY FLOW (130D) = LAG([MSUM(ACCUM2DSTRB_BASE,130D) / MSUM(VOLUME,130D)],5D)
        WHERE: ACCUM2DSTRB_BASE = [CLV_BASE * VOLUME] = [(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_130D_LAG5D = LAG(MMEAN(ACCUM2DSTRB_BASE, 130D) / MMEAN(VOLUME, 130D),5D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf = self._CMF(
            prc_lib=prc_lib, freq="WEEKDAY", periods=130, dates_keyspace=dates_keyspace
        ).shift1d(periods=5, keyspace=dates_keyspace, **kwds_args)
        if freq != "WEEKDAY":
            cmf = cmf.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf

    @RootLib.temp_frame()
    def CMF_130D_LAG10D(self, field, **kwds_args):
        """CMF_130D_LAG10D = CHAIKIN'S MONEY FLOW (130D) = LAG([MSUM(ACCUM2DSTRB_BASE,130D) / MSUM(VOLUME,130D)],10D)
        WHERE: ACCUM2DSTRB_BASE = [CLV_BASE * VOLUME] = [(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_130D_LAG10D = LAG(MMEAN(ACCUM2DSTRB_BASE, 130D) / MMEAN(VOLUME, 130D),10D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf = self._CMF(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=130,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        ).shift1d(periods=10, keyspace=dates_keyspace)
        if freq != "WEEKDAY":
            cmf = cmf.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf

    @RootLib.temp_frame()
    def CMF_130D_LAG22D(self, field, **kwds_args):
        """CMF_130D_LAG22D = CHAIKIN'S MONEY FLOW (65D) = LAG([MSUM(ACCUM2DSTRB_BASE,130D) / MSUM(VOLUME,130D)],22D)
        WHERE: ACCUM2DSTRB_BASE = [CLV_BASE * VOLUME] = [(((CLOSE - LOW) - (HIGH - CLOSE)) / (HIGH - LOW)) * VOLUME]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_130D_LAG22D = LAG(MMEAN(ACCUM2DSTRB_BASE, 130D) / MMEAN(VOLUME, 130D),22D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf = self._CMF(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=130,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        ).shift1d(periods=22, keyspace=dates_keyspace)
        if freq != "WEEKDAY":
            cmf = cmf.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf

    @RootLib.temp_frame()
    def CMF_5D65D(self, field, **kwds_args):
        """CMF_5D65D = CHAIKIN'S HISTORICALLY-ADJUSTED MONEY FLOW (5D) RELATIVE TO IT'S 65D AVERAGE = CMF_5D / MMEAN(CMF_5D,65D)
        WHERE: CMF_5D = CHAIKIN'S MONEY FLOW (5D) = [MSUM(ACCUM2DSTRB_BASE,5D) / MSUM(VOLUME,5D)]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_5D65D = CMF_5D / MMEAN(CMF_5D,65D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf_rel = self._CMF_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=5,
            rel_periods=65,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            cmf_rel = cmf_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf_rel

    @RootLib.temp_frame()
    def CMF_22D261D(self, field, **kwds_args):
        """CMF_22D261D = CHAIKIN'S HISTORICALLY-ADJUSTED MONEY FLOW (22D) RELATIVE TO IT'S 261D AVERAGE = CMF_22D / MMEAN(CMF_22D,261D)
        WHERE: CMF_22D = CHAIKIN'S MONEY FLOW (22D) = [MSUM(ACCUM2DSTRB_BASE,22D) / MSUM(VOLUME,22D)]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_22D261D = CMF_22D / MMEAN(CMF_22D,261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf_rel = self._CMF_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=22,
            rel_periods=261,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            cmf_rel = cmf_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf_rel

    @RootLib.temp_frame()
    def CMF_65D261D(self, field, **kwds_args):
        """CMF_65D261D = CHAIKIN'S HISTORICALLY-ADJUSTED MONEY FLOW (65D) RELATIVE TO IT'S 261D AVERAGE = CMF_65D / MMEAN(CMF_65D,261D)
        WHERE: CMF_65D = CHAIKIN'S MONEY FLOW (65D) = [MSUM(ACCUM2DSTRB_BASE,65D) / MSUM(VOLUME,65D)]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_65D261D = CMF_65D / MMEAN(CMF_65D,261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf_rel = self._CMF_REL(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=65,
            rel_periods=261,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            cmf_rel = cmf_rel.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf_rel

    @RootLib.temp_frame()
    def CMF_DIFF5D65D(self, field, **kwds_args):
        """CMF_5D65D = CHAIKIN'S HISTORICALLY-ADJUSTED MONEY FLOW (5D) DIFFERENCE OVRE PAST 65 DAYS = CMF_5D / MMEAN(CMF_5D,65D)
        WHERE: CMF_5D = CHAIKIN'S MONEY FLOW (5D) = [MSUM(ACCUM2DSTRB_BASE,5D) / MSUM(VOLUME,5D)]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_5D65D = MDIFF(CMF_5D,65D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf_diff = self._CMF_DIFF(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=5,
            rel_periods=65,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )

        if freq != "WEEKDAY":
            cmf_diff = cmf_diff.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf_diff

    @RootLib.temp_frame()
    def CMF_DIFF22D261D(self, field, **kwds_args):
        """CMF_22D261D = CHAIKIN'S HISTORICALLY-ADJUSTED MONEY FLOW (22D) DIFFERENCE OVRE PAST 261 DAYS = CMF_22D / MMEAN(CMF_22D,261D)
        WHERE: CMF_22D = CHAIKIN'S MONEY FLOW (22D) = [MSUM(ACCUM2DSTRB_BASE,22D) / MSUM(VOLUME,22D)]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_22D261D = MDIFF(CMF_22D,261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf = self._CMF(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=22,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        ).mdiff1d(periods=261, keyspace=dates_keyspace)

        cmf_diff = self._CMF_DIFF(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=22,
            rel_periods=261,
            dates_keyspace=dates_keyspace,
        )
        if freq != "WEEKDAY":
            cmf_diff = cmf_diff.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf_diff

    @RootLib.temp_frame()
    def CMF_DIFF65D261D(self, field, **kwds_args):
        """CMF_65D261D = CHAIKIN'S HISTORICALLY-ADJUSTED MONEY FLOW (65D) RDIFFERENCE OVRE PAST 261 DAYS = CMF_65D / MMEAN(CMF_65D,261D)
        WHERE: CMF_65D = CHAIKIN'S MONEY FLOW (65D) = [MSUM(ACCUM2DSTRB_BASE,65D) / MSUM(VOLUME,65D)]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:CMF_65D261D = MDIFF(CMF_65D,261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        cmf_diff = self._CMF_DIFF(
            prc_lib=prc_lib,
            freq="WEEKDAY",
            periods=65,
            rel_periods=261,
            dates_keyspace=dates_keyspace,
            **kwds_args,
        )
        if freq != "WEEKDAY":
            cmf_diff = cmf_diff.asfreq(freq=freq, keyspace=dates_keyspace)
        return cmf_diff

    @RootLib.temp_frame()
    def RSI_22D(self, field, **kwds_args):
        """RSI_22D = RELATIVE STRENGTH INDICATOR (PAST 22 DAYS) = [100 - (100/(1+RS))]
        WHERE: RS =[AVE_GAIN_22D / AVE_LOSS_22D]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:RSI_22D = [MAVE(TRET_D[TRET>=0],22) / MAVE(TRET_D[TRET<0],22)] = [AVE_GAIN_22D / AVE_LOSS_22D]
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        tret_gains = self.get_calendarized_field(
            field_prefix="TRET", freq="WEEKDAY", lib=prc_lib
        )
        tret_losses = tret_gains.copy()  # <-- Need a deep copy here!!!

        # Isolate positive tret_gains
        tret_gains.conditional_remove_inplace(tret_gains < 0.0)

        # Isolate negative tret_losses
        tret_losses.conditional_remove_inplace(tret_losses >= 0.0)

        ave_gain = tret_gains.mmean1d(
            22, keyspace=dates_keyspace, pct_required=0.0, ignore_missing=True
        )
        ave_loss = -1.0 * tret_losses.mmean1d(
            22, keyspace=dates_keyspace, pct_required=0.0, ignore_missing=True
        )  # Note: -1x TO MAKE SIGN OF LOSSES REFLECT POSITIVE VALUES
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        rs = ave_gain / ave_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))

        if freq != "WEEKDAY":
            rsi = rsi.asfreq(freq=freq, keyspace=dates_keyspace)
        return rsi

    @RootLib.temp_frame()
    def RSI_65D(self, field, **kwds_args):
        """RSI_22D = RELATIVE STRENGTH INDICATOR (PAST 65 DAYS) = [100 - (100/(1+RS))]
        WHERE: RS =[AVE_GAIN_65D / AVE_LOSS_65D]
        Prior:HIGH LEVEL = BULLISH"""
        # FL:RSI_65D = [MAVE(TRET_D[TRET>=0],65) / MAVE(TRET_D[TRET<0],65)] = [AVE_GAIN_65D / AVE_LOSS_65D]
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        tret_gains = self.get_calendarized_field(
            field_prefix="TRET", freq="WEEKDAY", lib=prc_lib
        )
        tret_losses = tret_gains.copy()  # <-- Need a deep copy here!!!

        # Isolate positive tret_gains
        tret_gains.conditional_remove_inplace(tret_gains < 0.0)

        # Isolate negative tret_losses
        tret_losses.conditional_remove_inplace(tret_losses >= 0.0)

        ave_gain = tret_gains.mmean1d(
            65, keyspace=dates_keyspace, pct_required=0.0, ignore_missing=True
        )
        ave_loss = -1.0 * tret_losses.mmean1d(
            65, keyspace=dates_keyspace, pct_required=0.0, ignore_missing=True
        )  # Note: -1x TO MAKE SIGN OF LOSSES REFLECT POSITIVE VALUES
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        rs = ave_gain / ave_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))

        if freq != "WEEKDAY":
            rsi = rsi.asfreq(freq=freq, keyspace=dates_keyspace)
        return rsi

    def _KLINGER_NORM(
        self,
        field,
        sum_periods,
        norm_periods,
        prc_lib,
        freq,
        dates_keyspace,
        rel_flag,
        **kwds_args,
    ):
        """KLINGER VOLUME OSCILLATOR FORMULA: SUMS UP-VOLUME MINUS DOWN-VOLUME

        NORMALIZED KLINGER VOLUME OSCILLATOR FORMULA:
        KLINGER_NORM = KLINGER VOLUME OSCILLATOR(sum_periods) / MSTD(KLINGER VOLUME OSCILLATOR(sum_periods), norm_periods)
        NOTE: INTENTIONALLY DID NOT INVOKE MZSCORE(norm_periods) ALGO...WANTED TO HONOR ANY BIAS IN MEAN (i.e., NOT DE-MEANED)
        """
        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )

        volume = self.get_calendarized_field(
            field_prefix="VOLUME", freq=freq, lib=prc_lib
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        if rel_flag:
            index_price_field = self.get_property(
                "index_price_field", field, grace=False, resolve_templates=True
            )
            index_price = RootLib()[index_price_field]
            if index_price is None:
                raise Exception(f"Could not procure market_index:{index_price_field}")
            elif index_price.is_empty:
                raise Exception(f"Empty market_index:{index_price_field}")
            elif dates_keyspace not in index_price.keyspaces:
                raise Exception(
                    f"index_price.keyspaces does not contain {dates_keyspace}"
                )
            elif dates_keyspace not in close.keyspaces:
                raise Exception(f"close.keyspaces does not contain {dates_keyspace}")

            # Massage index_price to align (freq & dates) with close
            index_price = index_price.fill1d(
                dates_keyspace, tfill_method="pad", tfill_max=5
            ).reindex1d(index=close, keyspace=dates_keyspace)
            rel_close = close / index_price
        else:
            rel_close = close

        rel_ret = (
            rel_close / rel_close.shift1d(periods=1, keyspace=dates_keyspace)
        ) - 1.0

        # Isolate up_volume
        up_volume = volume.conditional_remove(rel_ret <= 0.0)

        up_volume_sum = up_volume.msum1d(
            sum_periods, keyspace=dates_keyspace, pct_required=0.0, ignore_missing=True
        )

        # Isolate down_volume
        down_volume = volume.conditional_remove(rel_ret >= 0.0)

        down_volume_sum = down_volume.msum1d(
            sum_periods, keyspace=dates_keyspace, pct_required=0.0, ignore_missing=True
        )

        RootLib().set_control(
            "ignore_add", True
        )  # <-- ONLY FOR LINE BELOW...In-case we have ALL up days (or all down days) where complement item in expressioin below is missing
        klinger = up_volume_sum - down_volume_sum

        klinger_mstd = klinger.mstd1d(
            norm_periods,
            keyspace=dates_keyspace,
            pct_required=0.50,
            ignore_missing=True,
        )
        RootLib().set_control("ignore_mult", False)
        klinger_norm = klinger / klinger_mstd

        return klinger_norm

    @RootLib.temp_frame()
    def KLINGER_22D_NORM261D(self, field, **kwds_args):
        """KLINGER_22D_NORM261D: 22-DAY KLINGER VOLUME OSCILLATOR NORMALIZED BY ITS 261-DAY TRAILING STANDARD DEVIATION
        KLINGER_22D_NORM261D = KLINGER(22D) / MSTD(KLINGER(22D),261D)
        NOTE: INTENTIONALLY DID NOT INVOKE MZSCORE() ALGO...WANTED TO HONOR ANY BIAS IN MEAN (i.e., NOT DE-MEANED)
        """
        # FL:KLINGER_22D_NORM261D = KLINGER(22D) / MSTD(KLINGER(22D),261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        klinger_norm = self._KLINGER_NORM(
            field=field,
            sum_periods=22,
            norm_periods=261,
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            rel_flag=False,
        )
        if freq != "WEEKDAY":
            klinger_norm = klinger_norm.asfreq(freq=freq, keyspace=dates_keyspace)
        return klinger_norm

    @RootLib.temp_frame()
    def KLINGER_65D_NORM261D(self, field, **kwds_args):
        """KLINGER_65D_NORM261D: 65-DAY KLINGER VOLUME OSCILLATOR NORMALIZED BY ITS 261-DAY TRAILING STANDARD DEVIATION
        KLINGER_65D_NORM261D = KLINGER(65D) / MSTD(KLINGER(65D),261D)
        NOTE: INTENTIONALLY DID NOT INVOKE MZSCORE() ALGO...WANTED TO HONOR ANY BIAS IN MEAN (i.e., NOT DE-MEANED)
        """
        # FL:KLINGER_65D_Z261D = KLINGER(65D) / MSTD(KLINGER(65D),261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        klinger_norm = self._KLINGER_NORM(
            field=field,
            sum_periods=65,
            norm_periods=261,
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            rel_flag=False,
        )
        if freq != "WEEKDAY":
            klinger_norm = klinger_norm.asfreq(freq=freq, keyspace=dates_keyspace)
        return klinger_norm

    @RootLib.temp_frame()
    def KLINGER_130D_NORM261D(self, field, **kwds_args):
        """KLINGER_130D_NORM261D: 130-DAY KLINGER VOLUME OSCILLATOR NORMALIZED BY ITS 261-DAY TRAILING STANDARD DEVIATION
        KLINGER_130D_NORM261D = KLINGER(130D) / MSTD(KLINGER(130D),261D)
        NOTE: INTENTIONALLY DID NOT INVOKE MZSCORE() ALGO...WANTED TO HONOR ANY BIAS IN MEAN (i.e., NOT DE-MEANED)
        """
        # FL:KLINGER_130D_NORM261D = KLINGER(130D) / MSTD(KLINGER(130D),261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        klinger_norm = self._KLINGER_NORM(
            field=field,
            sum_periods=130,
            norm_periods=261,
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            rel_flag=False,
        )
        if freq != "WEEKDAY":
            klinger_norm = klinger_norm.asfreq(freq=freq, keyspace=dates_keyspace)
        return klinger_norm

    @RootLib.temp_frame()
    def KLINGER_1Y_NORM3Y(self, field, **kwds_args):
        """KLINGER_1Y_NORM3Y: 1-YEAR KLINGER VOLUME OSCILLATOR NORMALIZED BY ITS 3-YEAR TRAILING STANDARD DEVIATION
        KLINGER_1Y_NORM3Y = KLINGER(261D) / MSTD(KLINGER(261D),3*261D)
        NOTE: INTENTIONALLY DID NOT INVOKE MZSCORE() ALGO...WANTED TO HONOR ANY BIAS IN MEAN (i.e., NOT DE-MEANED)
        """
        # FL:KLINGER_1Y_NORM3Y = KLINGER(261D) / MSTD(KLINGER(261D),(3*261D))
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        klinger_norm = self._KLINGER_NORM(
            field=field,
            sum_periods=261,
            norm_periods=(3 * 261),
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            rel_flag=False,
        )
        if freq != "WEEKDAY":
            klinger_norm = klinger_norm.asfreq(freq=freq, keyspace=dates_keyspace)
        return klinger_norm

    @RootLib.temp_frame()
    def REL_KLINGER_22D_NORM261D(self, field, **kwds_args):
        """REL_KLINGER_22D_NORM261D: 22-DAY KLINGER VOLUME OSCILLATOR [USING MKT REL RETURNS] NORMALIZED BY ITS 261-DAY TRAILING STANDARD DEVIATION
        REL_KLINGER_22D_NORM261D = KLINGER(22D) / MSTD(KLINGER(22D),261D)
        NOTE: INTENTIONALLY DID NOT INVOKE MZSCORE() ALGO...WANTED TO HONOR ANY BIAS IN MEAN (i.e., NOT DE-MEANED)
        """
        # FL:REL_KLINGER_22D_NORM261D = KLINGER(22D) / MSTD(KLINGER(22D),261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        klinger_norm = self._KLINGER_NORM(
            field=field,
            sum_periods=22,
            norm_periods=261,
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            rel_flag=True,
        )
        if freq != "WEEKDAY":
            klinger_norm = klinger_norm.asfreq(freq=freq, keyspace=dates_keyspace)
        return klinger_norm

    @RootLib.temp_frame()
    def REL_KLINGER_65D_NORM261D(self, field, **kwds_args):
        """REL_KLINGER_65D_NORM261D: 65-DAY KLINGER VOLUME OSCILLATOR [USING MKT REL RETURNS] NORMALIZED BY ITS 261-DAY TRAILING STANDARD DEVIATION
        REL_KLINGER_65D_NORM261D = KLINGER(65D) / MSTD(KLINGER(65D),261D)
        NOTE: INTENTIONALLY DID NOT INVOKE MZSCORE() ALGO...WANTED TO HONOR ANY BIAS IN MEAN (i.e., NOT DE-MEANED)
        """
        # FL:REL_KLINGER_65D_Z261D = KLINGER(65D) / MSTD(KLINGER(65D),261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        klinger_norm = self._KLINGER_NORM(
            field=field,
            sum_periods=65,
            norm_periods=261,
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            rel_flag=True,
        )
        if freq != "WEEKDAY":
            klinger_norm = klinger_norm.asfreq(freq=freq, keyspace=dates_keyspace)
        return klinger_norm

    @RootLib.temp_frame()
    def REL_KLINGER_130D_NORM261D(self, field, **kwds_args):
        """REL_KLINGER_130D_NORM261D: 130-DAY KLINGER VOLUME OSCILLATOR [USING MKT REL RETURNS] NORMALIZED BY ITS 261-DAY TRAILING STANDARD DEVIATION
        REL_KLINGER_130D_NORM261D = KLINGER(130D) / MSTD(KLINGER(130D),261D)
        NOTE: INTENTIONALLY DID NOT INVOKE MZSCORE() ALGO...WANTED TO HONOR ANY BIAS IN MEAN (i.e., NOT DE-MEANED)
        """
        # FL:KLINGER_130D_NORM261D = KLINGER(130D) / MSTD(KLINGER(130D),261D)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        klinger_norm = self._KLINGER_NORM(
            field=field,
            sum_periods=130,
            norm_periods=261,
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            rel_flag=True,
        )
        if freq != "WEEKDAY":
            klinger_norm = klinger_norm.asfreq(freq=freq, keyspace=dates_keyspace)
        return klinger_norm

    @RootLib.temp_frame()
    def REL_KLINGER_1Y_NORM3Y(self, field, **kwds_args):
        """REL_KLINGER_1Y_NORM3Y: 1-YEAR KLINGER VOLUME OSCILLATOR [USING MKT REL RETURNS] NORMALIZED BY ITS 3-YEAR TRAILING STANDARD DEVIATION
        REL_KLINGER_1Y_NORM3Y = KLINGER(130D) / MSTD(KLINGER(65D),261D)
        NOTE: INTENTIONALLY DID NOT INVOKE MZSCORE() ALGO...WANTED TO HONOR ANY BIAS IN MEAN (i.e., NOT DE-MEANED)
        """
        # FL:REL_KLINGER_1Y_NORM3Y = KLINGER(261D) / MSTD(KLINGER(261D),(3*261D))
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        klinger_norm = self._KLINGER_NORM(
            field=field,
            sum_periods=261,
            norm_periods=(3 * 261),
            prc_lib=prc_lib,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
            rel_flag=True,
        )
        if freq != "WEEKDAY":
            klinger_norm = klinger_norm.asfreq(freq=freq, keyspace=dates_keyspace)
        return klinger_norm

    def _BOLL(
        self,
        periods,
        prc_lib,
        freq,
        dates_keyspace,
        pct_required=0.5,
        ignore_missing=True,
    ):
        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        return close.mz1d(
            periods,
            keyspace=dates_keyspace,
            pct_required=pct_required,
            ignore_missing=ignore_missing,
        )

    @RootLib.temp_frame()
    def BOLL_5D(self, field, **kwds_args):
        """BOLL_5D = (CLOSE - MMEAN(CLOSE,5D)) / MSTD(CLOSE,5D)"""
        # FL:BOLL_5D = (CLOSE - MMEAN(CLOSE,5BD)) / MSTD(CLOSE,5BD)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        boll = self._BOLL(
            periods=5, prc_lib=prc_lib, freq="WEEKDAY", dates_keyspace=dates_keyspace
        )
        if freq != "WEEKDAY":
            boll = boll.asfreq(freq=freq, keyspace=dates_keyspace)
        return boll

    @RootLib.temp_frame()
    def BOLL_22D(self, field, **kwds_args):
        """BOLL_22D = (CLOSE - MMEAN(CLOSE,22D)) / MSTD(CLOSE,22D)"""
        # FL:BOLL_22D = (CLOSE - MMEAN(CLOSE,22BD)) / MSTD(CLOSE,22BD)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        boll = self._BOLL(
            periods=22, prc_lib=prc_lib, freq="WEEKDAY", dates_keyspace=dates_keyspace
        )
        if freq != "WEEKDAY":
            boll = boll.asfreq(freq=freq, keyspace=dates_keyspace)
        return boll

    @RootLib.temp_frame()
    def BOLL_4W(self, field, **kwds_args):
        """BOLL_4W = (CLOSE - MMEAN(CLOSE,4W)) / MSTD(CLOSE,4W)"""
        # FL:BOLL_4W = (CLOSE - MMEAN(CLOSE,4W)) / MSTD(CLOSE,4W)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        boll = self._BOLL(
            periods=4, prc_lib=prc_lib, freq=weekly_freq, dates_keyspace=dates_keyspace
        )
        if freq != weekly_freq:
            boll = boll.asfreq(freq=freq, keyspace=dates_keyspace)
        return boll

    @RootLib.temp_frame()
    def BOLL_150D(self, field, **kwds_args):
        """BOLL_150D = (CLOSE - MMEAN(CLOSE,150D)) / MSTD(CLOSE,150D)"""
        # FL:BOLL_150D = (CLOSE - MMEAN(CLOSE,150BD)) / MSTD(CLOSE,150BD)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        boll = self._BOLL(
            periods=150, prc_lib=prc_lib, freq="WEEKDAY", dates_keyspace=dates_keyspace
        )
        if freq != "WEEKDAY":
            boll = boll.asfreq(freq=freq, keyspace=dates_keyspace)
        return boll

    @RootLib.temp_frame()
    def BOLL_30W(self, field, **kwds_args):
        """BOLL_30W = (CLOSE - MMEAN(CLOSE,30W)) / MSTD(CLOSE,30W)"""
        # FL:BOLL_30W = (CLOSE - MMEAN(CLOSE,30W)) / MSTD(CLOSE,30W)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        boll = self._BOLL(
            periods=30, prc_lib=prc_lib, freq=weekly_freq, dates_keyspace=dates_keyspace
        )
        if freq != weekly_freq:
            boll = boll.asfreq(freq=freq, keyspace=dates_keyspace)
        return boll

    @RootLib.temp_frame()
    def BOLL_7M(self, field, **kwds_args):
        """BOLL_7M = (CLOSE - MMEAN(CLOSE,7M)) / MSTD(CLOSE,7M)"""
        # FL:BOLL_7M = (CLOSE - MMEAN(CLOSE,7M)) / MSTD(CLOSE,7M)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        boll = self._BOLL(
            periods=7, prc_lib=prc_lib, freq="CEOM", dates_keyspace=dates_keyspace
        )
        if freq != "CEOM":
            boll = boll.asfreq(freq=freq, keyspace=dates_keyspace)
        return boll

    # @RootLib.temp_frame()
    def _FORCE_INDEX(self, prc_lib, cft_lib, fiscal_mode, freq, **kwds_args):
        """FORCE_INDEX = (TRET_D*VOLUME/SHARES)"""
        # DL:FORCE_INDEX = (TRET_D*VOLUME/SHARES)
        tret = self.get_calendarized_field(field_prefix="TRET", freq=freq, lib=prc_lib)

        # VOLUME is provided in Shares (NOT Millions of Shares)
        volume = self.get_calendarized_field(
            field_prefix="VOLUME", freq=freq, lib=prc_lib
        )

        # SHARES are provided in Millions of Shares...convert to shares convention for comparison w/VOLUME
        shares = 1000000.0 * self.get_fiscal_field(
            field_prefix="SHARES", fiscal_mode=fiscal_mode, lib=cft_lib, freq=freq
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        force_index = tret * volume / shares
        return force_index

    # @RootLib.temp_frame()
    def _FORCE2_INDEX(
        self, prc_lib, cft_lib, fiscal_mode, freq, dates_keyspace, **kwds_args
    ):
        """FORCE2_INDEX = ((CLOSE-CLOSE_LAG1D)*VOLUME/MV)"""
        # DL:FORCE2_INDEX = ((CLOSE-CLOSE(T-1))*VOLUME/MV)

        close = self.get_calendarized_field(
            field_prefix="CLOSE",
            freq=freq,
            lib=prc_lib,
            tfill_method_dict={"WEEKDAY": "pad"},
            tfill_max_dict={"WEEKDAY": 5},
        )
        close_lag1d = close.shift1d(1, keyspace=dates_keyspace)

        # VOLUME is provided in Shares (NOT Millions of Shares)
        volume = self.get_calendarized_field(
            field_prefix="VOLUME", freq=freq, lib=prc_lib
        )

        # MKTCAP is provided in Millions of $...convert to $ convention for comparison w/(PRICE * VOLUME)
        mv = 1000000.0 * self.get_calendarized_field(
            field_prefix="MKTCAP", freq=freq, lib=self
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")
        force_index2 = (close - close_lag1d) * volume / mv
        return force_index2

    @RootLib.temp_frame()
    def FORCE_AVE10D(self, field, **kwds_args):
        """FORCE_AVE10D: 10D AVERAGE OF FORCE INDEX
        WHERE: FORCE_INDEX = (TRET_D*VOLUME/SHARES)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE10D = MAVE(FORCE_IDX,10) = MAVE((TRET_D*VOLUME/SHARES),10)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        force = self._FORCE_INDEX(
            prc_lib=prc_lib, cft_lib=cft_lib, fiscal_mode=fiscal_mode, freq="WEEKDAY"
        )
        result = force.mmean1d(
            periods=10, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE_AVE22D(self, field, **kwds_args):
        """FORCE_AVE22D: 22D AVERAGE OF FORCE INDEX
        WHERE: FORCE_INDEX = (TRET_D*VOLUME/SHARES)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE22D = MAVE(FORCE_IDX,22) = MAVE((TRET_D*VOLUME/SHARES),22)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        force = self._FORCE_INDEX(
            prc_lib=prc_lib, cft_lib=cft_lib, fiscal_mode=fiscal_mode, freq="WEEKDAY"
        )
        result = force.mmean1d(
            periods=22, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE_AVE4W(self, field, **kwds_args):
        """FORCE_AVE4W: 4W AVERAGE OF FORCE INDEX
        WHERE: FORCE_INDEX = (TRET_D*VOLUME/SHARES)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE4W = MAVE(FORCE_IDX,4W) = MAVE((TRET_D*VOLUME/SHARES),4W)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        force = self._FORCE_INDEX(
            prc_lib=prc_lib, cft_lib=cft_lib, fiscal_mode=fiscal_mode, freq=weekly_freq
        )
        result = force.mmean1d(
            periods=4, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != weekly_freq:
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE_AVE65D(self, field, **kwds_args):
        """FORCE_AVE65D: 65D AVERAGE OF FORCE INDEX
        WHERE: FORCE_INDEX = (TRET_D*VOLUME/SHARES)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE65D = MAVE(FORCE_IDX,65) = MAVE((TRET_D*VOLUME/SHARES),65)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        force = self._FORCE_INDEX(
            prc_lib=prc_lib, cft_lib=cft_lib, fiscal_mode=fiscal_mode, freq="WEEKDAY"
        )
        result = force.mmean1d(
            periods=65, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE_AVE13W(self, field, **kwds_args):
        """FORCE_AVE13W: 13W AVERAGE OF FORCE INDEX
        WHERE: FORCE_INDEX = (TRET_D*VOLUME/SHARES)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE13W = MAVE(FORCE_IDX,13W) = MAVE((TRET_D*VOLUME/SHARES),13W)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        force = self._FORCE_INDEX(
            prc_lib=prc_lib, cft_lib=cft_lib, fiscal_mode=fiscal_mode, freq=weekly_freq
        )
        result = force.mmean1d(
            periods=13, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != weekly_freq:
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE_AVE3M(self, field, **kwds_args):
        """FORCE_AVE3M: 3M AVERAGE OF FORCE INDEX
        WHERE: FORCE_INDEX = (TRET_D*VOLUME/SHARES)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE3M = MAVE(FORCE_IDX,3M) = MAVE((TRET_D*VOLUME/SHARES),3M)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        force = self._FORCE_INDEX(
            prc_lib=prc_lib, cft_lib=cft_lib, fiscal_mode=fiscal_mode, freq="CEOM"
        )
        result = force.mmean1d(
            periods=3, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != "CEOM":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE2_AVE10D(self, field, **kwds_args):
        """FORCE2_AVE10D: 10D AVERAGE OF FORCE2 INDEX
        WHERE: FORCE2_INDEX = (CLOSE[T]-CLOSE[T-1])*VOLUME/MV)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE10D = MAVE(FORCE2_IDX,10) = MAVE((CLOSE[T]-CLOSE[T-1])*VOLUME/MV),10)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        force2 = self._FORCE2_INDEX(
            prc_lib=prc_lib,
            cft_lib=cft_lib,
            fiscal_mode=fiscal_mode,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
        )
        result = force2.mmean1d(
            periods=10, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE2_AVE22D(self, field, **kwds_args):
        """FORCE2_AVE22D: 22D AVERAGE OF FORCE2 INDEX
        WHERE: FORCE2_INDEX = = (CLOSE[T]-CLOSE[T-1])*VOLUME/MV)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE22D = MAVE(FORCE2_IDX,22) = MAVE((CLOSE[T]-CLOSE[T-1])*VOLUME/MV),22)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        force2 = self._FORCE2_INDEX(
            prc_lib=prc_lib,
            cft_lib=cft_lib,
            fiscal_mode=fiscal_mode,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
        )
        result = force2.mmean1d(
            periods=22, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE2_AVE4W(self, field, **kwds_args):
        """FORCE2_AVE4W: 4W AVERAGE OF FORCE2 INDEX
        WHERE: FORCE2_INDEX = = (CLOSE[T]-CLOSE[T-1])*VOLUME/MV)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE4W = MAVE(FORCE2_IDX,4W) = MAVE((CLOSE[T]-CLOSE[T-1])*VOLUME/MV),4W)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        force2 = self._FORCE2_INDEX(
            prc_lib=prc_lib,
            cft_lib=cft_lib,
            fiscal_mode=fiscal_mode,
            freq=weekly_freq,
            dates_keyspace=dates_keyspace,
        )
        result = force2.mmean1d(
            periods=4, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != weekly_freq:
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE2_AVE65D(self, field, **kwds_args):
        """FORCE2_AVE65D: 65D AVERAGE OF FORCE2 INDEX
        WHERE: FORCE2_INDEX = = (CLOSE[T]-CLOSE[T-1])*VOLUME/MV)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE65D = MAVE(FORCE2_IDX,65) = MAVE((CLOSE[T]-CLOSE[T-1])*VOLUME/MV),65)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        force2 = self._FORCE2_INDEX(
            prc_lib=prc_lib,
            cft_lib=cft_lib,
            fiscal_mode=fiscal_mode,
            freq="WEEKDAY",
            dates_keyspace=dates_keyspace,
        )
        result = force2.mmean1d(
            periods=65, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE2_AVE13W(self, field, **kwds_args):
        """FORCE2_AVE13W: 13W AVERAGE OF FORCE2 INDEX
        WHERE: FORCE2_INDEX = = (CLOSE[T]-CLOSE[T-1])*VOLUME/MV)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE13W = MAVE(FORCE2_IDX,13W) = MAVE((CLOSE[T]-CLOSE[T-1])*VOLUME/MV),13W)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        force2 = self._FORCE2_INDEX(
            prc_lib=prc_lib,
            cft_lib=cft_lib,
            fiscal_mode=fiscal_mode,
            freq=weekly_freq,
            dates_keyspace=dates_keyspace,
        )
        result = force2.mmean1d(
            periods=13, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != weekly_freq:
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def FORCE2_AVE3M(self, field, **kwds_args):
        """FORCE2_AVE3M: 3M AVERAGE OF FORCE2 INDEX
        WHERE: FORCE2_INDEX = = (CLOSE[T]-CLOSE[T-1])*VOLUME/MV)
        NOTE: Have introduced shares in denominator of force index
              to make the force measure comparable across stocks
        """
        # FL:FORCE_AVE3M = MAVE(FORCE2_IDX,3M) = MAVE((CLOSE[T]-CLOSE[T-1])*VOLUME/MV),3M)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        cft_lib = self.get_property("cft_lib", field, grace=False)
        fiscal_mode = self.get_property(
            "fiscal_mode", field, grace=True, default_property_value="FQ"
        )
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        force2 = self._FORCE2_INDEX(
            prc_lib=prc_lib,
            cft_lib=cft_lib,
            fiscal_mode=fiscal_mode,
            freq="CEOM",
            dates_keyspace=dates_keyspace,
        )
        result = force2.mmean1d(
            periods=13, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        if freq != "CEOM":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def VOLUME_SPIKE_22D261D(self, field, **kwds_args):
        """VOLUME_SPIKE_22D261D: ABNORMALLY HIGH ST AVERAGE VOLUME AS COMPARED TO LT AVERAGE VOLUME
        Similar to "Visibility Ratio" and related to "High Volume Premium" from Gervais, Simon & Migelgrin (2001)
        Prior: HIGH VALUE = BULLISH (High Volume Premium)"
        """
        # FL:VOLUME_SPIKE_22D261D = MAVE(DLR_VOLUME,22) / MAVE(DLR_VOLUME,261)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq="WEEKDAY", lib=prc_lib
        )

        dlr_volume_short_mave = dlr_volume.mmean1d(
            periods=22, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        dlr_volume_long_mave = dlr_volume.mmean1d(
            periods=261, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume_short_mave / dlr_volume_long_mave
        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def VOLUME_SPIKE_4W52W(self, field, **kwds_args):
        """VOLUME_SPIKE_4W52W: ABNORMALLY HIGH ST AVERAGE VOLUME AS COMPARED TO LT AVERAGE VOLUME
        Similar to "Visibility Ratio" and related to "High Volume Premium" from Gervais, Simon & Migelgrin (2001)
        Prior: HIGH VALUE = BULLISH (High Volume Premium)"
        """
        # FL:VOLUME_SPIKE_4W52W = MAVE(DLR_VOLUME,4W) / MAVE(DLR_VOLUME,52W)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq=weekly_freq, lib=prc_lib
        )

        dlr_volume_long_mave = dlr_volume.mmean1d(
            periods=12, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume / dlr_volume_long_mave
        if freq != weekly_freq:
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def VOLUME_SPIKE_1M12M(self, field, **kwds_args):
        """VOLUME_SPIKE_1M12M: ABNORMALLY HIGH ST AVERAGE VOLUME AS COMPARED TO LT AVERAGE VOLUME
        Similar to "Visibility Ratio" and related to "High Volume Premium" from Gervais, Simon & Migelgrin (2001)
        Prior: HIGH VALUE = BULLISH (High Volume Premium)"
        """
        # FL:VOLUME_SPIKE_1M12M = MAVE(DLR_VOLUME,1M) / MAVE(DLR_VOLUME,12M)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq="CEOM", lib=prc_lib
        )

        dlr_volume_long_mave = dlr_volume.mmean1d(
            periods=12, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume / dlr_volume_long_mave
        if freq != "CEOM":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def ABNORM_DAV_22D261D(self, field, **kwds_args):
        """ABNORM_DAV_22D261D: ABNORMALLY HIGH ST AVERAGE DOLLAR VOLUME AS COMPARED TO LT STDDEV OF DOLLAR VOLUME
        Related to "Visibility Ratio" and related to "High Volume Premium" from Gervais, Simon & Migelgrin (2001)
        Prior: HIGH VALUE = BULLISH (High Volume Premium)"
        """
        # FL:ABNORM_DAV_22D261D = MAVE(DLR_VOLUME,22) / MSTD(DLR_VOLUME,261)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq="WEEKDAY", lib=prc_lib
        )

        dlr_volume_short_mave = dlr_volume.mmean1d(
            periods=22, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        dlr_volume_long_std = dlr_volume.mstd1d(
            periods=261, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume_short_mave / dlr_volume_long_std

        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def ABNORM_DAV_4W52W(self, field, **kwds_args):
        """ABNORM_DAV_4W52W: ABNORMALLY HIGH ST AVERAGE DOLLAR VOLUME AS COMPARED TO LT STDDEV OF DOLLAR VOLUME
        Related to "Visibility Ratio" and related to "High Volume Premium" from Gervais, Simon & Migelgrin (2001)
        Prior: HIGH VALUE = BULLISH (High Volume Premium)"
        """
        # FL:ABNORM_DAV_4W52W = MAVE(DLR_VOLUME,4W) / MSTD(DLR_VOLUME,52W)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq=weekly_freq, lib=prc_lib
        )

        dlr_volume_short_mave = dlr_volume.mmean1d(
            periods=4, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        dlr_volume_long_std = dlr_volume.mstd1d(
            periods=52, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume_short_mave / dlr_volume_long_std

        if freq != weekly_freq:
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def ABNORM_DAV_1M12M(self, field, **kwds_args):
        """ABNORM_DAV_1M12M: ABNORMALLY HIGH ST AVERAGE DOLLAR VOLUME AS COMPARED TO LT STDDEV OF DOLLAR VOLUME
        Related to "Visibility Ratio" and related to "High Volume Premium" from Gervais, Simon & Migelgrin (2001)
        Prior: HIGH VALUE = BULLISH (High Volume Premium)"
        """
        # FL:ABNORM_DAV_1M12M = MAVE(DLR_VOLUME,1M) / MSTD(DLR_VOLUME,12M)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq="CEOM", lib=prc_lib
        )

        dlr_volume_long_std = dlr_volume.mstd1d(
            periods=12, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume / dlr_volume_long_std

        if freq != "CEOM":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def NORM_DVVOL_65D(self, field, **kwds_args):
        """NORM_DVVOL_65D: NORMALIZED DOLLAR VOLUME VOLATILITY (PAST 65 DAYS)
        Prior: HIGH VALUE = BEARISH (High Volume Premium? as denominator is lower and result higher for low liquidity)"
        """
        # FL:NORM_DVVOL_65D = MSTD(DLR_VOLUME,65) / MEDIAN(DLR_VOLUME,65)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq="WEEKDAY", lib=prc_lib
        )

        dlr_volume_mstd = dlr_volume.mstd1d(
            periods=65, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        dlr_volume_mmedian = dlr_volume.mmedian1d(
            periods=65, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume_mstd / dlr_volume_mmedian

        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def NORM_DVVOL_13W(self, field, **kwds_args):
        """NORM_DVVOL_13W: NORMALIZED DOLLAR VOLUME VOLATILITY (PAST 13 WEEKS)
        Prior: HIGH VALUE = BEARISH (High Volume Premium? as denominator is lower and result higher for low liquidity)"
        """
        # FL:NORM_DVVOL_13W = MSTD(DLR_VOLUME,13W) / MEDIAN(DLR_VOLUME,13W)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq=weekly_freq, lib=prc_lib
        )

        dlr_volume_mstd = dlr_volume.mstd1d(
            periods=13, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        dlr_volume_mmedian = dlr_volume.mmedian1d(
            periods=13, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume_mstd / dlr_volume_mmedian

        if freq != weekly_freq:
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def NORM_DVVOL_3M(self, field, **kwds_args):
        """NORM_DVVOL_3M: NORMALIZED DOLLAR VOLUME VOLATILITY (PAST 3 MONTHS)
        Prior: HIGH VALUE = BEARISH (High Volume Premium? as denominator is lower and result higher for low liquidity)"
        """
        # FL:NORM_DVVOL_3M = MSTD(DLR_VOLUME,3M) / MEDIAN(DLR_VOLUME,3M)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq="CEOM", lib=prc_lib
        )

        dlr_volume_mstd = dlr_volume.mstd1d(
            periods=3, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        dlr_volume_mmedian = dlr_volume.mmedian1d(
            periods=3, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume_mstd / dlr_volume_mmedian

        if freq != "CEOM":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def NORM_DVVOL_261D(self, field, **kwds_args):
        """NORM_DVVOL_261D: NORMALIZED DOLLAR VOLUME VOLATILITY (PAST 261 DAYS)
        Prior: HIGH VALUE = BEARISH (High Volume Premium? as denominator is lower and result higher for low liquidity)"
        """
        # FL:NORM_DVVOL_261D = MSTD(DLR_VOLUME,261) / MEDIAN(DLR_VOLUME,261)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq="WEEKDAY", lib=prc_lib
        )

        dlr_volume_mstd = dlr_volume.mstd1d(
            periods=261, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        dlr_volume_mmedian = dlr_volume.mmedian1d(
            periods=261, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume_mstd / dlr_volume_mmedian

        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def NORM_DVVOL_52W(self, field, **kwds_args):
        """NORM_DVVOL_52W: NORMALIZED DOLLAR VOLUME VOLATILITY (PAST 52 WEEKS)
        Prior: HIGH VALUE = BEARISH (High Volume Premium? as denominator is lower and result higher for low liquidity)"
        """
        # FL:NORM_DVVOL_52W = MSTD(DLR_VOLUME,52W) / MEDIAN(DLR_VOLUME,52W)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        weekly_freq = self.get_property(
            "weekly_freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq=weekly_freq, lib=prc_lib
        )

        dlr_volume_mstd = dlr_volume.mstd1d(
            periods=52, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        dlr_volume_mmedian = dlr_volume.mmedian1d(
            periods=52, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume_mstd / dlr_volume_mmedian

        if freq != weekly_freq:
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def NORM_DVVOL_12M(self, field, **kwds_args):
        """NORM_DVVOL_12M: NORMALIZED DOLLAR VOLUME VOLATILITY (PAST 12 MONTHS)
        Prior: HIGH VALUE = BEARISH (High Volume Premium? as denominator is lower and result higher for low liquidity)"
        """
        # FL:NORM_DVVOL_12M = MSTD(DLR_VOLUME,12M) / MEDIAN(DLR_VOLUME,12M)
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dlr_volume = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq="CEOM", lib=prc_lib
        )

        dlr_volume_mstd = dlr_volume.mstd1d(
            periods=12, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        dlr_volume_mmedian = dlr_volume.mmedian1d(
            periods=12, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dlr_volume_mstd / dlr_volume_mmedian

        if freq != "CEOM":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def DVVOL2MVVOL_22D(self, field, **kwds_args):
        """DVVOL2MVVOL_22D: RATIO OF (22 DAY) DOLLAR VOLUME VOLATILITY TO (22 DAY) MARKET VALUE VOLATILITY
        Prior: HIGH VALUE = BEARISH (Reverse of High Volume Premium)"
        """
        # FL:DVVOL2MVVOL_22D = DV_VOL22D / MV_VOL22D
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dv = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq="WEEKDAY", lib=prc_lib
        ).convert_fx("USD")
        mv = self.get_calendarized_field(
            field_prefix="MKTCAP", freq="WEEKDAY", lib=self
        ).convert_fx("USD")

        dv_vol = dv.mstd1d(
            periods=22, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        mv_vol = mv.mstd1d(
            periods=22, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dv_vol / mv_vol

        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

    @RootLib.temp_frame()
    def DVVOL2MVVOL_65D(self, field, **kwds_args):
        """DVVOL2MVVOL_22D: RATIO OF (65 DAY) DOLLAR VOLUME VOLATILITY TO (65 DAY) MARKET VALUE VOLATILITY
        Prior: HIGH VALUE = BEARISH (Reverse of High Volume Premium)"
        """
        # FL:DVVOL2MVVOL_65D = DVVOL65D / MVVOL65D
        prc_lib = self.get_property("prc_lib", field, grace=False)
        freq = self.get_property(
            "freq", field, grace=True, resolve_templates=True
        )  # <-- Do not assign default (as we want to allow some fiscal fields to have freq=None)
        dates_keyspace = self.get_property(
            "dates_keyspace", field, grace=True, default_property_value="Dates"
        )

        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        RootLib().set_control("auto_compress", True)
        RootLib().set_control("variate_mode", "uni")

        dv = self.get_calendarized_field(
            field_prefix="DLR_VOLUME", freq="WEEKDAY", lib=prc_lib
        ).convert_fx("USD")
        mv = self.get_calendarized_field(
            field_prefix="MKTCAP", freq="WEEKDAY", lib=self
        ).convert_fx("USD")

        dv_vol = dv.mstd1d(
            periods=65, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )
        mv_vol = mv.mstd1d(
            periods=65, keyspace=dates_keyspace, pct_required=0.5, ignore_missing=True
        )

        result = dv_vol / mv_vol

        if freq != "WEEKDAY":
            result = result.asfreq(freq=freq, keyspace=dates_keyspace)
        return result

        ## =================================== OPTIONS MARKET SENTIMENT FACTORS (23) =======================================


