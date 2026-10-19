#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SaveIndicatorTests(unittest.TestCase):
    def test_blank_after_irq_lock_before_erase_and_preserve_rejection(self) -> None:
        source = (ROOT / "firmware/src/smk37_app.c").read_text()
        start = source.index("static int smk37_storage_erase(uint32_t off)")
        end = source.index("static int smk37_storage_program", start)
        adapter = source[start:end]
        harness = r"""
#include <assert.h>
#include <stdint.h>
#include <string.h>
#define SMK37_ENABLE_SAVES 1
#define FL_RANGE_OK(off,n) ((off)>=0xeb000u && (off)<=0xf3000u && (n)<=0xf3000u-(off))
#define FL_FAR(fn) (fn)
static int smk37_storage_writable=1,locked,blanked,erases,result;
static uint8_t smk37_dma[64];
static uint32_t irq_save(void){assert(!locked);locked=1;return 7;}
static void irq_restore(uint32_t f){assert(locked && f==7);locked=0;}
static void smk37_indicators_blank(void){assert(locked);blanked=1;}
static int fl_erase4k_ram(uint32_t off,uint32_t *took){
    assert(off==0xeb000u && locked && blanked);
    for(unsigned i=0;i<sizeof smk37_dma;++i)assert(!smk37_dma[i]);
    ++erases;*took=17000;return result;
}
static int fl_erase4k(uint32_t off,uint32_t *took){
    uint32_t f=irq_save();int rc=fl_erase4k_ram(off,took);irq_restore(f);return rc;
}
"""
        scenarios = r"""
int main(void){
    assert(smk37_storage_erase(0x4000u)==-1);
    assert(smk37_storage_erase(0xeb001u)==-1);
    assert(smk37_storage_erase(0xf3000u)==-1);
    assert(!erases && !blanked && !locked);
    smk37_storage_writable=0;assert(smk37_storage_erase(0xeb000u)==-1);
    assert(!erases && !blanked && !locked);smk37_storage_writable=1;
    for(result=0;result>=-4;result-=4){
        blanked=0;memset(smk37_dma,0x5a,sizeof smk37_dma);
        assert(smk37_storage_erase(0xeb000u)==result);
        assert(blanked && !locked);
    }
    assert(erases==2);return 0;
}
"""
        with tempfile.TemporaryDirectory(prefix="smk-save-led-") as directory:
            path = Path(directory)
            (path / "test.c").write_text(harness + adapter + scenarios)
            subprocess.run(
                [os.environ.get("CC", "cc"), "-std=c99", "-O1", str(path / "test.c"), "-o", str(path / "test")],
                check=True,
            )
            subprocess.run([str(path / "test")], check=True)


if __name__ == "__main__":
    unittest.main()
