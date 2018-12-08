#!/usr/bin/python3

# Copyright 2018 Timothy Baldwin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
here = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(here, "lib"))

import product_converter as pc
import repository

sys.setrecursionlimit(10000)
pc.have_closed = False
pc.repo = repository.Repository("super")
pc.submodules = "submodules"
pc.submodules_out = os.path.abspath(pc.submodules)

pc.merge_branches(pc.convert("BCM2835Dev"  ), pc.convert("BCM2835"  ))
pc.merge_branches(pc.convert("BuildHostDev"), pc.convert("BuildHost"))
pc.merge_branches(pc.convert("DiscDev"     ), pc.convert("Disc"     ))
pc.merge_branches(pc.convert("iMx6Dev"     ), pc.convert("iMx6"     ))
pc.merge_branches(pc.convert("IOMDHALDev"  ), pc.convert("IOMDHAL"  ))
pc.merge_branches(pc.convert("OMAP3Dev"    ), pc.convert("OMAP3"    ))
pc.merge_branches(pc.convert("OMAP4Dev"    ), pc.convert("OMAP4"    ))
pc.merge_branches(pc.convert("TitaniumDev" ), pc.convert("Titanium" ))
pc.merge_branches(pc.convert("TungstenDev" ), pc.convert("Tungsten" ))

pc.convert("BCM2835Pico" )
pc.convert("Batch1to6Dev")
pc.convert("BonusBinDev" )
pc.convert("OMAP3Live"   )
pc.convert("OMAP5Dev"    )
pc.convert("S3CDev"      )
pc.convert("PlingSystem" )

#pc.convert("CTools"      )

print("Saving...")
pc.repo.save()
