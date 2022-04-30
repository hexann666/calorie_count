from sysconfig import is_python_build
from testbook import testbook

@testbook('00_core.ipynb')
def test_name_checking(tb):
    with tb.patch(
        "ipykernel.kernelbase.Kernel.raw_input",
        side_effect=[170, 86, 41, 'm'],
    ) as mock_input:
        tb.execute_cell("name_checking")
        assert tb.cell_output_text("name_checking") == "Your name is Harry Potter."