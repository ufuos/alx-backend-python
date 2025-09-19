# 🧪 Unit Tests for `utils`

This repository contains **unit tests** for two utility functions:

- `access_nested_map`: Safely access values inside nested dictionaries using a sequence of keys.
- `get_json`: Fetch JSON data from a given HTTP endpoint.

The tests are written with the **Python `unittest` framework**, and use:

- [`parameterized`](https://github.com/wolever/parameterized) for running the same test with different inputs.
- [`unittest.mock`](https://docs.python.org/3/library/unittest.mock.html) for mocking HTTP requests.

---

## 📂 Files

- `test_utils.py` → Contains the unit tests.
- `utils.py` → Contains the actual function implementations (not shown here).

---

## ⚡ Features Tested

1. **`TestAccessNestedMap`**

   - Valid paths return the correct values.
   - Invalid paths raise `KeyError` with the correct missing key.

2. **`TestGetJson`**
   - HTTP requests are mocked, so no external calls are made.
   - Ensures `requests.get` is called correctly.
   - Verifies that `get_json` returns the expected payload.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```
