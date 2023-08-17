# Linear Regression

## Resources

- [Video](https://youtu.be/aEPoLeS6UMM)
- [Session 49 - PDF](https://drive.google.com/file/d/18oSjN8aEztz_m-_CoKb5i_kGHvKccjdp/view?usp=share_link)
- [Day48 Simple Linear Regression](https://github.com/campusx-official/100-days-of-machine-learning/tree/main/day48-simple-linear-regression)
- [Day49 Regression Metrics](https://github.com/campusx-official/100-days-of-machine-learning/tree/main/day49-regression-metrics)
- [Session 50 Notebook](https://colab.research.google.com/github/campusx-official/100-days-of-machine-learning/blob/main/day50-multiple-linear-regression/multiple_linear_regression.ipynb#scrollTo=NpAvnU-t3yV0)
- [Session 50 Notebook - 2](https://colab.research.google.com/github/campusx-official/100-days-of-machine-learning/blob/main/day50-multiple-linear-regression/code-from-scratch.ipynb#scrollTo=afc9a715)
- [Session 50 - PDF](https://drive.google.com/file/d/1fYGa7wXCirq8Tvo2YqfHsQSlhs1DXXwo/view?usp=share_link)

## Topics

**Practice topics [in Code](./notebook)**

### Simple Linear Regression

Used to create relationship between target feature and only one input feature.

> [!IMPORTANT]
>
> **For Example,** if have data of college student CGPA and LPA salary after placement of the student as input feature. The Linear Regression model tries to create relationship between these two features by plotting a regression line on the graph which pass through all the points in such a way that **the residuals/error between the line and points is least**.

| $m = \text{Slope of Regression Line}$                                                                                         | $b = \text{Intercept of Regression Line}$ |
| ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| $$m = \frac{\displaystyle\sum_{i=1}^{n} {(x_i - \bar{x}) (y_i - \bar{y})}}{\displaystyle\sum_{i=1}^{n} {(x_i - \bar{x})^2}}$$ | $$b = \bar{y} - m \cdot \bar{x}$$         |

$$f(x) = m \cdot x + b$$

### Multiple Linear Regression

This method used to model the relationship between multiple independent variables (features) and a dependent variable (response) using a linear equation. The general form of a multiple linear regression model with $(p)$ independent variables is:

$$Y = \beta{_0} + \beta{_1}X_1 + \beta{_2}X_2 + \ldots + \beta{_p}X_p + \varepsilon$$

Where:

- $(Y)$ is the dependent variable (response).
- $(X_1, X_2, \ldots, X_p)$ are the independent variables (features).
- $(\beta{_0}, \beta{_1}, \beta{_2}, \ldots, \beta{_p})$ are the coefficients that represent the impact of each independent variable on the dependent variable.
- $(\varepsilon)$ is the error term, representing the unexplained variation in the dependent variable.

This equation can be expressed in matrix notation as follows:

$$[ \mathbf{Y} = \mathbf{X} \beta + \mathbf{\varepsilon} ]$$

**Where:**

- $(\mathbf{Y})$ is the vector of observed values of the dependent variable.
- $(\mathbf{X})$ is the design matrix containing the observed values of the independent variables.
- $(\beta)$ is the vector of coefficients.
- $(\mathbf{\varepsilon})$ is the vector of error terms.

In matrix notation, the model is typically written as:

$$
\begin{bmatrix}
y_1 \\
y_2 \\
\vdots \\
y_n
\end{bmatrix} = \begin{bmatrix}
1 & x_{11} & x_{12} & \ldots & x_{1p} \\
1 & x_{21} & x_{22} & \ldots & x_{2p} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_{n1} & x_{n2} & \ldots & x_{np}
\end{bmatrix} \begin{bmatrix}
\beta{_0} \\
\beta{_1} \\
\beta{_2} \\
\vdots \\
\beta{_p}
\end{bmatrix} + \begin{bmatrix}
\varepsilon{_1} \\
\varepsilon{_2} \\
\vdots \\
\varepsilon{_n}
\end{bmatrix}
$$

To estimate the coefficients $(\beta)$, the least squares method is commonly used. The goal is to minimize the sum of squared differences between the observed values $(\mathbf{Y})$ and the values predicted by the model $(\mathbf{X} \beta)$:

$$\text{minimize} |{\mathbf{Y} - \mathbf{X} \beta}|^2$$

The least squares solution for $(\beta)$ is given by:

$$\beta = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{Y}$$

**Where:**

- $((\mathbf{X}^T \mathbf{X})^{-1})$ is the inverse of the matrix $(\mathbf{X}^T \mathbf{X})$.
- $(\mathbf{X}^T)$ is the transpose of the matrix $(\mathbf{X})$.
- $(\mathbf{Y})$ is the vector of observed values of the dependent variable.

This solution gives us the estimated coefficients $(\beta)$ that best fit the data in a least squares sense.

In summary, multiple linear regression uses matrices to express the relationships between multiple independent variables and a dependent variable. The goal is to find the coefficients that minimize the sum of squared differences between the observed and predicted values. The least squares method provides a way to estimate these coefficients using matrix operations.
