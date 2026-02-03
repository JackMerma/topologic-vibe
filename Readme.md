This demo works with python version > 3.10
If you have problems with sklearn library in the moment to install requirements, please execute in Linux:

```bash
export SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL=True
```

or in Windows:

```bash
$env:SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL="True"
```


Once you save the notebook version, it will be saved as app.py, and you will need to execute this command to run the app locally:

```bash
streamlit run app.py
```
