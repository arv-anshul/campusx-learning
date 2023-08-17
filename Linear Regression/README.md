# Linear Regression

## Resources

- [Video](https://youtu.be/aEPoLeS6UMM)
- [PDF](https://drive.google.com/file/d/18oSjN8aEztz_m-_CoKb5i_kGHvKccjdp/view?usp=share_link)
- [Day48 Simple Linear Regression](https://github.com/campusx-official/100-days-of-machine-learning/tree/main/day48-simple-linear-regression)
- [Day49 Regression Metrics](https://github.com/campusx-official/100-days-of-machine-learning/tree/main/day49-regression-metrics)

## Topics

**Practice topics [in Code](./notebook)**

### Simple Linear Regression

Used to create relationship between target feature and only one input feature.

> [!IMPORTANT]
>
> **For Example,** if have data of college student CGPA and LPA salary after placement of the student as input feature. The Linear Regression model tries to create relationship between these two features by plotting a regression line on the graph which pass through all the points in such a way that **the residuals/error between the line and points is least**.

| $m = \text{Slope of Regression Line}$                                                                                       | $b = \text{Intercept of Regression Line}$ |
| --------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| $m = \frac{\displaystyle\sum_{i=1}^{n} {(x_i - \bar{x}) (y_i - \bar{y})}}{\displaystyle\sum_{i=1}^{n} {(x_i - \bar{x})^2}}$ | $b = \bar{y} - m \cdot \bar{x}$           |

$$f(x) = m \cdot x + b$$
