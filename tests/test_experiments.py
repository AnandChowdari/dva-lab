"""Unit tests for experiment code retrieval, execution, and shortcuts."""

import pytest
import sys
from pathlib import Path

# Set non-interactive Matplotlib backend before importing pyplot
import matplotlib
matplotlib.use("Agg")

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import dva_lab
import matplotlib.pyplot as plt


@pytest.fixture(autouse=True)
def cleanup_figures():
    """Ensure all figures are closed after each test to prevent memory leaks."""
    yield
    plt.close("all")


# ----------------------------------------------------------------------------
# Code Retrieval Tests
# ----------------------------------------------------------------------------

@pytest.mark.parametrize("number", range(1, 13))
def test_get_code_returns_non_empty_code(number):
    """Ensure get_code() returns valid source code for all experiments."""
    code = dva_lab.get_code(number)
    assert isinstance(code, str)
    assert len(code.strip()) > 50


def test_get_code_expected_keywords():
    """Verify code contains experiment-specific authoritative keywords."""
    assert "sales_cube" in dva_lab.get_code(1)
    assert "dim_product" in dva_lab.get_code(2) or "time_id" in dva_lab.get_code(2)
    assert "plt.bar" in dva_lab.get_code(3)
    assert "bottom=" in dva_lab.get_code(4)
    assert "plt.hist" in dva_lab.get_code(5)
    assert "kdeplot" in dva_lab.get_code(6)
    assert "ECDF" in dva_lab.get_code(7)
    assert "probplot" in dva_lab.get_code(8)
    assert "plt.scatter" in dva_lab.get_code(9)
    assert "sales_data.csv" in dva_lab.get_code(10)
    assert "Profit Margin %" in dva_lab.get_code(11)
    assert "Sales Level" in dva_lab.get_code(12)


# ----------------------------------------------------------------------------
# Markdown Display Tests
# ----------------------------------------------------------------------------

@pytest.mark.parametrize("number", range(1, 13))
def test_show_experiment_returns_markdown(number):
    """Ensure show_experiment() generates complete markdown documentation."""
    md = dva_lab.show_experiment(number)
    assert f"Experiment {number}:" in md
    assert "### Aim" in md
    assert "### Concept & Methodology" in md
    assert "### Complete Source Code" in md
    assert "### Expected Output" in md
    assert "### Result Statement" in md


# ----------------------------------------------------------------------------
# Python Execution Tests (Experiments 3 to 9)
# ----------------------------------------------------------------------------

def test_run_experiment_3_bar_charts():
    """Test vertical and horizontal bar charts execution."""
    fig1, fig2 = dva_lab.run_experiment(3, show=False)
    assert fig1 is not None
    assert fig2 is not None

    # Test side by side layout
    fig_combined = dva_lab.run_experiment(3, show=False, side_by_side=True)
    assert fig_combined is not None


def test_run_experiment_4_grouped_stacked():
    """Test grouped and stacked bar charts execution."""
    fig1, fig2 = dva_lab.run_experiment(4, show=False)
    assert fig1 is not None
    assert fig2 is not None

    fig_combined = dva_lab.run_experiment(4, show=False, side_by_side=True)
    assert fig_combined is not None


def test_run_experiment_5_histograms():
    """Test single and multi-variable histograms execution."""
    fig1, fig2 = dva_lab.run_experiment(5, show=False)
    assert fig1 is not None
    assert fig2 is not None

    fig_combined = dva_lab.run_experiment(5, show=False, side_by_side=True)
    assert fig_combined is not None


def test_run_experiment_6_density():
    """Test single and multi-variable density plots execution."""
    fig1, fig2 = dva_lab.run_experiment(6, show=False)
    assert fig1 is not None
    assert fig2 is not None

    fig_combined = dva_lab.run_experiment(6, show=False, side_by_side=True)
    assert fig_combined is not None


def test_run_experiment_7_ecdf():
    """Test ECDF plot execution."""
    fig = dva_lab.run_experiment(7, show=False)
    assert fig is not None


def test_run_experiment_8_qq_plot():
    """Test Q-Q plot execution."""
    fig = dva_lab.run_experiment(8, show=False)
    assert fig is not None


def test_run_experiment_9_scatter():
    """Test scatter plot execution."""
    fig = dva_lab.run_experiment(9, show=False)
    assert fig is not None


# ----------------------------------------------------------------------------
# Shortcut Functions Tests (exp1 through exp12)
# ----------------------------------------------------------------------------

def test_all_shortcuts_exist_and_run():
    """Verify shortcut functions exp1() through exp12() operate properly."""
    # SQL shortcuts do not raise and return code/notice
    sql1 = dva_lab.exp1(show_sql=False)
    assert "sales_cube" in sql1

    sql2 = dva_lab.exp2(show_sql=False)
    assert "time_id" in sql2

    # Python plotting shortcuts
    f3 = dva_lab.exp3(show=False)
    assert f3 is not None
    f4 = dva_lab.exp4(show=False)
    assert f4 is not None
    f5 = dva_lab.exp5(show=False)
    assert f5 is not None
    f6 = dva_lab.exp6(show=False)
    assert f6 is not None
    f7 = dva_lab.exp7(show=False)
    assert f7 is not None
    f8 = dva_lab.exp8(show=False)
    assert f8 is not None
    f9 = dva_lab.exp9(show=False)
    assert f9 is not None

    # Power BI shortcuts
    p10 = dva_lab.exp10(show_preview=False)
    assert "sales_data.csv" in p10
    p11 = dva_lab.exp11(show_simulation=False)
    assert "Total Sales" in p11
    p12 = dva_lab.exp12(show_simulation=False)
    assert "Sales Level" in p12


# ----------------------------------------------------------------------------
# Power BI and Data Helper Tests
# ----------------------------------------------------------------------------

def test_load_sales_data():
    """Verify sales_data.csv loads correctly with exact 10 records."""
    df = dva_lab.load_sales_data()
    assert len(df) == 10
    expected_cols = [
        "OrderID", "OrderDate", "Region", "Category", "Product",
        "Quantity", "UnitPrice", "UnitCost", "Sales"
    ]
    for col in expected_cols:
        assert col in df.columns
    assert df["Sales"].sum() == 29900


def test_powerbi_python_simulations():
    """Test python simulation functions for DAX calculations."""
    from dva_lab.experiments.exp11_powerbi_dax import simulate_in_python as sim11
    from dva_lab.experiments.exp12_powerbi_logic import simulate_in_python as sim12

    df11 = sim11()
    assert len(df11) == 5  # 4 regions + Total
    total_sales = df11.loc[df11["Region"] == "Total", "Total Sales"].values[0]
    total_profit = df11.loc[df11["Region"] == "Total", "Total Profit"].values[0]
    assert total_sales == 29900
    assert total_profit == 8050

    df12 = sim12()
    assert len(df12) == 10
    assert "Sales Level" in df12.columns
    assert "Bulk East Order" in df12.columns
    assert "Focus Order" in df12.columns
    assert (df12["Focus Order"] == "Yes").sum() == 5


# ----------------------------------------------------------------------------
# Help / About and Error Handling Tests
# ----------------------------------------------------------------------------

def test_about_and_help(capsys):
    """Verify about() / help() runs without errors."""
    dva_lab.about()
    captured = capsys.readouterr()
    assert "dva-lab" in captured.out
    assert "list_experiments" in captured.out


@pytest.mark.parametrize("invalid_num", [0, 13, 99])
def test_invalid_experiment_number_errors(invalid_num):
    """Verify ValueError is raised across public functions for invalid experiment number."""
    with pytest.raises(ValueError):
        dva_lab.show_experiment(invalid_num)
    with pytest.raises(ValueError):
        dva_lab.get_code(invalid_num)
    with pytest.raises(ValueError):
        dva_lab.run_experiment(invalid_num)
