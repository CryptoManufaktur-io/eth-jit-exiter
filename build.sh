# eth2spec's setup.py tries to locate the file tests/core/pyspec/eth2spec/VERSION.txt
# which breaks when running under the pyinstaller packed mode.
# As a workaround, we temporarily create the path it expects.
mkdir eth2spec
touch eth2spec/VERSION.txt

poetry run pyinstaller \
--onefile \
--collect-data eth2spec \
--collect-data eth_jit_exiter ./eth_jit_exiter/main.py \
--name eth-jit-exiter \
--distpath build/eth-jit-exiter

rm -rf eth2spec
