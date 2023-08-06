## What?

`streamlit-kpi-metric` library function is to facilitate display of key-point indicators to dashboards.

---

## WHY?

- Effective KPIs are important metrics to make sure that you can summerize and pay attention to important indicators.
  
- Library makes it easy to generate KPI with different labels to mention important figures.

---

## HOW?
    
- ### Install library to respective project's `pyproject.toml`

```zsh
poetry add streamlit-kpi-metrics
```

- ### Importing function to parsing scripts

```python
from streamlit_kpi_metrics import metric, metric_row
```

 - ### Implementing function
  Write following code to a file `main.py`

```python
st.write("## Solo Metric")
metric("Metric 0", 150)

st.write("## Multiple Metric")
metric_row(
    {
        "Metric 1": 10,
        "Metric 2": 20,
        "Metric 3": 30,
        "Metric 4": 40,
        "Metric 5": 50,
    }
)
```

- ### Running file 

```zsh 
poetry run streamlit run main.py
```

--- 

- ### Output of the mentioned code 
![](./static/streamlit-metric-image.png)

---