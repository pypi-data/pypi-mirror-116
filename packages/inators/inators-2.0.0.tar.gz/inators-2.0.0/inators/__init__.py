# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import pkg_resources

from . import arg
from . import imp
from . import log


__version__ = pkg_resources.get_distribution(__package__).version

del pkg_resources
