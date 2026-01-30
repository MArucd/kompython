import json
import os
import sys
from datetime import datetime

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

pytest_plugins = ["pytest_snapshot"]

# ВСЕ! Больше никаких event_loop, anyio и прочей хуйни

def pytest_configure(config):
    """Инициализация тестов"""
    if not hasattr(config, "workerinput"):
        with open("parsing_results.json", "w") as f:
            json.dump(
                {"timestamp": datetime.now().isoformat(), "results": {}},
                f,
                ensure_ascii=False,
                indent=2,
            )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняем результаты"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        try:
            import importlib
            test_module = importlib.import_module(item.module.__name__)
            
            if hasattr(test_module, 'get_test_results'):
                all_results_data = test_module.get_test_results()

                if all_results_data:
                    try:
                        with open("parsing_results.json", "r") as f:
                            all_results = json.load(f)
                    except (FileNotFoundError, json.JSONDecodeError):
                        all_results = {
                            "timestamp": datetime.now().isoformat(),
                            "results": {},
                        }

                    all_results["results"].update(all_results_data)

                    with open("parsing_results.json", "w", encoding="utf-8") as f:
                        json.dump(all_results, f, ensure_ascii=False, indent=2)
        except (ImportError, AttributeError):
            pass