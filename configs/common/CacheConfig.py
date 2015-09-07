# Copyright (c) 2010 Advanced Micro Devices, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Lisa Hsu

# Configure the M5 cache hierarchy config in one place
#

import m5
from m5.objects import *
from Caches import *
from O3_ARM_v7a import *

class L3Config(object):
    def __init__( self, options, system ):
        self.options = options
        self.system = system
        self.latencies = {
            '4096kB' : '8.48ns',
            '3072kB' : '7.5',
            '2048kB' : '6.5ns',
            '1792kB' : '6.5ns',
            '1536kB' : '6.5ns',
            '1280kB' : '6.5ns',
            '1024kB' : '6.5ns',
            '768kB'  : '6.5ns',
            '512kB'  : '6.5ns',
            '256kB'  : '6.5ns',
            '1920kB' : '6.5ns',
            '1664kB' : '6.5ns',
            '1408kB' : '6.5ns',
            '1152kB' : '6.5ns',
            '896kB' : '6.5ns',
            '640kB'  : '6.5ns',
            '384kB'  : '6.5ns',
            '128kB'  : '6.5ns',
            '1kB'    : '6.5ns',
        }

    def connect_l2( self ): return

class L3Shared( L3Config ):
    def __init__( self, options, system ):
        super( L3Shared, self ).__init__( options, system )
        system.l3 = L3Cache(size = options.l3_size, 
                            latency=self.latencies[options.l3_size],
                            assoc = options.l3_assoc,
                            block_size=options.cacheline_size)

        system.tol3bus = NoncoherentBus()
        system.l3.cpu_side = system.tol3bus.master
        system.l3.mem_side = system.membus.slave

    def connect_l2( self ):
        for i in xrange( self.options.num_cpus ):
            self.system.l2[i].mem_side = self.system.tol3bus.slave

class L3Private( L3Config ):
    def __init__( self, options, system ):
        super( L3Private , self ).__init__( options, system )
        system.l3 = [
                L3Cache(
                    size = options.l3_size,
                    latency = self.latencies[options.l3_size],
                    assoc = options.l3_assoc,
                    block_size = options.cacheline_size
                )
                for i in xrange( options.num_cpus )
            ]

        system.tol3bus = [NoncoherentBus() for i in xrange( options.num_cpus ) ]

        for i in xrange( options.num_cpus ):
            system.l3[i].cpu_side = system.tol3bus[i].master
            system.l3[i].mem_side = system.membus.slave

    def connect_l2( self ):
        for i in xrange( self.options.num_cpus ):
            self.system.l2[i].mem_side = self.system.tol3bus[i].slave

class L2Config(object):
    def __init__( self, options, system ):
        self.options = options
        self.system = system
        self.latencies = {
            '4096kB' : '8.48ns',
            '3072kB' : '7.5',
            '2048kB' : '6.5ns',
            '1792kB' : '6.5ns',
            '1536kB' : '6.5ns',
            '1280kB' : '6.5ns',
            '1024kB' : '6.5ns',
            '768kB'  : '6.5ns',
            '512kB'  : '6.5ns',
            '256kB'  : '6.5ns',
            '1920kB' : '6.5ns',
            '1664kB' : '6.5ns',
            '1408kB' : '6.5ns',
            '1152kB' : '6.5ns',
            '896kB' : '6.5ns',
            '640kB'  : '6.5ns',
            '384kB'  : '6.5ns',
            '128kB'  : '6.5ns',
            '1kB'    : '6.5ns',
        }

    def connect_l1( self, system ): return

class L2Shared( L2Config ):
    def __init__( self, options, system ):
        super( L2Shared, self ).__init__( options, system )
        system.l2 = L2Cache(size = options.l2_size, 
                            latency=self.latencies[options.l2_size],
                            assoc = options.l2_assoc,
                            block_size=options.cacheline_size,
                            partition_cache=options.partition_cache,
                            dynamic_cache=options.dynamic_cache,
                            util_cache=options.util_cache,
                            lattice_cache=options.lattice_cache,
                            diamond_cache=options.diamond_cache,
                            L_assoc=options.L_assoc,
                            H_min=options.H_min,
                            th_inc=options.th_inc,
                            th_dec=options.th_dec,
                            num_tcs=options.numpids)

        system.tol2bus = NoncoherentBus()
        system.l2.cpu_side = system.tol2bus.master
        system.l2.mem_side = system.membus.slave

    def connect_l1( self, system ):
        for i in xrange( self.options.num_cpus ):
            system.cpu[i].connectAllPorts(system.tol2bus)

class L2Private( L2Config ):
    def __init__( self, options, system ):
        super( L2Private , self ).__init__( options, system )
        system.l2 = [
                L2Cache(
                    size = options.l2_size,
                    latency = self.latencies[options.l2_size],
                    assoc = options.l2_assoc,
                    block_size = options.cacheline_size
                )
                for i in xrange( options.num_cpus )
            ]

        system.tol2bus = [NoncoherentBus() for i in xrange( options.num_cpus ) ]

        for i in xrange( options.num_cpus ):
            system.l2[i].cpu_side = system.tol2bus[i].master
            self.system.l2[i].mem_side = system.membus.slave

    def connect_l1( self, system ):
        for i in xrange( self.options.num_cpus ):
            system.cpu[i].connectAllPorts(system.tol2bus[i])
            
def config_cache(options, system):

    #-------------------------------------------------------------------------
    # L1
    #-------------------------------------------------------------------------
    for i in xrange(options.num_cpus):
        if options.caches:
            icache = L1Cache(size = options.l1i_size,
                             assoc = options.l1i_assoc,
                             block_size=options.cacheline_size)
            dcache = L1Cache(size = options.l1d_size,
                             assoc = options.l1d_assoc,
                             block_size=options.cacheline_size)

            if buildEnv['TARGET_ISA'] == 'x86':
                system.cpu[i].addPrivateSplitL1Caches(icache, dcache,
                                                      PageTableWalkerCache(),
                                                      PageTableWalkerCache())
            else:
                system.cpu[i].addPrivateSplitL1Caches(icache, dcache)
        system.cpu[i].createInterruptController()

    #-------------------------------------------------------------------------
    # L2
    #-------------------------------------------------------------------------
    if options.l2cache:
        if options.l2config == "shared":
            l2config = L2Shared( options, system )
        else:
            l2config = L2Private( options, system )
        l2config.connect_l1( system )

    #-------------------------------------------------------------------------
    # L3
    #-------------------------------------------------------------------------
    if options.l3cache:
        if options.l3config == "shared":
            l3config = L3Shared( options, system )
        else:
            l3config = L3Private( options, system )
        if options.l3cache:
            l3config.connect_l2()

    return system
