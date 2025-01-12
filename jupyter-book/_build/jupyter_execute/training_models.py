#!/usr/bin/env python
# coding: utf-8

# (ch:trainingModels)=
# # 모델 훈련

# **감사의 글**
# 
# 자료를 공개한 저자 오렐리앙 제롱과 강의자료를 지원한 한빛아카데미에게 진심어린 감사를 전합니다.

# **소스코드**
# 
# 본문 내용의 일부를 파이썬으로 구현한 내용은 
# [(구글코랩) 모델 훈련](https://colab.research.google.com/github/codingalzi/handson-ml3/blob/master/notebooks/code_training_models.ipynb)에서 
# 확인할 수 있다.

# **주요 내용**
# 
# * 선형 회귀 모델 구현
#     * 선형대수 활용
#     * 경사하강법 활용
# * 경사하강법 종류
#     * 배치 경사하강법
#     * 미니배치 경사하강법
#     * 확률적 경사하강법(SGD)
# * 다항 회귀: 비선형 회귀 모델
# * 학습 곡선: 과소, 과대 적합 감지
# * 모델 규제: 과대 적합 방지
# * 로지스틱 회귀와 소프트맥스 회귀: 분류 모델

# **목표**
# 
# 모델 훈련의 기본 작동 과정과 원리를 살펴보며,
# 이를 통해 다음 사항들에 대한 이해를 넓힌다.
# 
# - 적정 모델 선택
# - 적정 훈련 알고리즘 선택
# - 적정 하이퍼파라미터 선택
# - 디버깅과 오차 분석
# - 신경망 구현 및 훈련 과정 이해

# ## 선형 회귀

# **선형 회귀 예제: 1인당 GDP와 삶의 만족도**

# {numref}`%s 절 <sec:model_based_learning>`에서 1인당 GDP와 삶의 만족도 사이의 
# 관계를 다음 1차 함수로 표현할 수 있었다.
# 
# $$(\text{삶의만족도}) = \theta_0 + \theta_1\cdot (\text{1인당GDP})$$
# 
# 즉, 1인당 GDP가 주어지면 위 함수를 이용하여 삶의 만족도를 예측하였다.
# 주어진 1인당 GDP를 **입력 특성**<font size="2">input feature</font> $x$, 
# 예측된 삶의 만족도를 **예측값** $\hat y$ 라 하면 다음 식으로 변환된다.
# 
# $$\hat y = \theta_0 + \theta_1\cdot x_1$$
# 
# 절편 $\theta_0$ 와 기울기 $\theta_1$ 은 (선형) 모델의 **파라미터**<font size="2">weight parameter</font>이다.
# 머신러닝에서는 절편은 **편향**<font size="2">bias</font>, 
# 기울기는 **가중치**<font size="2">weight</font> 라 부른다.
# 
# 따라서 1인당 GDP와 삶의 만족도 사이의 선형 관계를 모델로 구현하려면
# 적절한 하나의 편향과 하나의 가중치, 즉 총 2개의 파라미터를 결정해야 한다.

# **선형 회귀 예제: 캘리포니아 주택 가격 예측**

# 반면에 {numref}`%s 장 <ch:end2end>`의 캘리포니아 주택 가격 예측 선형 회귀 모델은
# 24개의 입력 특성을 사용하는 다음 함수를 이용한다.
# 
# $$\hat y = \theta_0 + \theta_1\cdot x_1 + \cdots + \theta_{24}\cdot x_{24}$$
# 
# * $\hat y$: 예측값
# * $x_i$: 구역의 $i$ 번째 특성값(위도, 경도, 중간소득, 가구당 인원 등등등)
# * $\theta_0$: 편향
# * $\theta_i$: $i$ 번째 특성에 대한 (가중치) 파라미터, 단 $i > 0$.
# 
# 따라서 캘리포니아의 구역별 중간 주택 가격을 예측하는 선형 회귀 모델을 구하려면 
# 적절한 하나의 편향과 24개의 가중치,
# 즉 총 25개의 파라미터를 결정해야 한다.

# **선형 회귀 함수**

# 이를 일반화하면 다음과 같다.
# 
# $$\hat y = \theta_0 + \theta_1\cdot x_1 + \cdots + \theta_{n}\cdot x_{n}$$
# 
# * $\hat y$: 예측값
# * $n$: 특성 수
# * $x_i$: 구역의 $i$ 번째 특성값
# * $\theta_0$: 편향
# * $\theta_j$: $j$ 번째 특성에 대한 (가중치) 파라미터(단, $1 \le j \le n$)
# 
# 일반적으로 선형 회귀 모델을 구현하려면
# 한 개의 편향과 $n$ 개의 가중치, 즉 총 $(1+n)$ 개의 파라미터를 결정해야 한다.

# **벡터 표기법**
# 
# 예측값을 벡터의 **내적**<font size="2">inner product</font>으로 표현할 수 있다.
# 
# $$
# \hat y
# = h_\theta (\mathbf{x})
# = \mathbf{\theta} \cdot \mathbf{x}
# $$
# 
# * $h_\theta(\cdot)$: 예측 함수, 즉 모델의 `predict()` 메서드.
# * $\mathbf{x} = (1, x_1, \dots, x_n)$
# * $\mathbf{\theta} = (\theta_0, \theta_1, \dots, \theta_n)$

# **2D 어레이 표기법**
# 
# 머신러닝에서는 훈련 샘플을 나타내는 입력 벡터와 파라미터 벡터를 일반적으로 아래 모양의 행렬로 나타낸다.
# 
# $$
# \mathbf{x}=
# \begin{bmatrix}
# 1 \\
# x_1 \\
# \vdots \\
# x_n
# \end{bmatrix},
# \qquad
# \mathbf{\theta}=
# \begin{bmatrix}
# \theta_0\\
# \theta_1 \\
# \vdots \\
# \theta_n
# \end{bmatrix}
# $$
# 
# 따라서 예측값은 다음과 같이 행렬 연산으로 표기된다.
# 단, $A^T$ 는 행렬 $A$의 전치행렬을 가리킨다.
# 
# $$
# \hat y
# = h_\theta (\mathbf{x})
# = \mathbf{\theta}^{T} \mathbf{x}
# $$

# **선형 회귀 모델의 행렬 연산 표기법**

# $\mathbf{X}$가 전체 입력 데이터셋, 즉 전체 훈련셋을 가리키는 (m, 1+n) 모양의 2D 어레이, 즉 행렬이라 하자.
# - $m$: 훈련셋의 크기.
# - $n$: 특성 수
# 
# 그러면 $\mathbf{X}$ 는 다음과 같이 표현된다.
# 단, $\mathbf{x}_j^{(i)}$ 는 $i$-번째 입력 샘플의 $j$-번째 특성값을 가리킨다.
# 
# $$
# \mathbf{X}= 
# \begin{bmatrix} 
# [1, \mathbf{x}_1^{(1)}, \dots, \mathbf{x}_n^{(1)}] \\
# \vdots \\
# [1, \mathbf{x}_1^{(m)}, \dots, \mathbf{x}_n^{(m)}] \\
# \end{bmatrix}
# $$

# 결론적으로 모든 입력값에 대한 예측값을 하나의 행렬식으로 표현하면 다음과 같다.

# $$
# \begin{bmatrix}
# \hat y_1 \\
# \vdots \\
# \hat y_m
# \end{bmatrix}
# = 
# \begin{bmatrix} 
# [1, \mathbf{x}_1^{(1)}, \dots, \mathbf{x}_n^{(1)}] \\
# \vdots \\
# [1, \mathbf{x}_1^{(m)}, \dots, \mathbf{x}_n^{(m)}] \\
# \end{bmatrix}
# \,\, 
# \begin{bmatrix}
# \theta_0\\
# \theta_1 \\
# \vdots \\
# \theta_n
# \end{bmatrix}
# $$

# 간략하게 줄이면 다음과 같다.

# $$
# \hat{\mathbf y} = \mathbf{X}\, \mathbf{\theta}
# $$

# 위 식에 사용된 기호들의 의미와 어레이 모양은 다음과 같다.
# 
# | 데이터 | 어레이 기호           |     어레이 모양(shape) | 
# |:-------------:|:-------------:|:---------------:|
# | 예측값 | $\hat{\mathbf y}$  | $(m, 1)$ |
# | 훈련셋 | $\mathbf X$   | $(m, 1+n)$     |
# | 파라미터 | $\mathbf{\theta}$      | $(1+n, 1)$ |

# **비용함수: 평균 제곱 오차(MSE)**

# 회귀 모델은 훈련 중에 **평균 제곱 오차**<font size="2">mean squared error</font>(MSE)를 이용하여
# 성능을 평가한다.

# $$
# \mathrm{MSE}(\mathbf{\theta}) := \mathrm{MSE}(\mathbf X, h_{\mathbf{\theta}}) = 
# \frac 1 m \sum_{i=1}^{m} \big(\mathbf{\theta}^{T}\, \mathbf{x}^{(i)} - y^{(i)}\big)^2
# $$

# 최종 목표는 훈련셋이 주어졌을 때 $\mathrm{MSE}(\mathbf{\theta})$가 최소가 되도록 하는 
# $\mathbf{\theta}$를 찾는 것이다.
# 
# * 방식 1: 정규방정식 또는 특이값 분해(SVD) 활용
#     * 드물지만 수학적으로 비용함수를 최소화하는 $\mathbf{\theta}$ 값을 직접 계산할 수 있는 경우 활용
#     * 계산복잡도가 $O(n^2)$ 이상인 행렬 연산을 수행해야 함. 
#     * 따라서 특성 수($n$)이 큰 경우 메모리 관리 및 시간복잡도 문제때문에 비효율적임.
# 
# * 방식 2: 경사하강법
#     * 특성 수가 매우 크거나 훈련 샘플이 너무 많아 메모리에 한꺼번에 담을 수 없을 때 적합
#     * 일반적으로 선형 회귀 모델 훈련에 적용되는 기법

# ### 정규 방정식

# 비용함수를 최소화 하는 $\theta$를 
# 정규 방정식<font size="2">normal equation</font>을 이용하여 
# 아래와 같이 바로 계산할 수 있다.
# 단, $\mathbf{X}^T\, \mathbf{X}$ 의 역행렬이 존재해야 한다.
# 
# $$
# \hat{\mathbf{\theta}} = 
# (\mathbf{X}^T\, \mathbf{X})^{-1}\, \mathbf{X}^T\, \mathbf{y}
# $$

# ### `LinearRegression` 클래스

# **SVD(특잇값 분해) 활용**
# 
# 그런데 행렬 연산과 역행렬 계산은 계산 복잡도가 $O(n^{2.4})$ 이상이며
# 항상 역행렬 계산이 가능한 것도 아니다.
# 반면에, **특잇값 분해**를 활용하여 얻어지는 
# **무어-펜로즈(Moore-Penrose) 유사 역행렬** $\mathbf{X}^+$은 항상 존재하며
# 계산 복잡도가 $O(n^2)$ 로 보다 빠른 계산을 지원한다.
# 또한 다음이 성립한다.
# 
# $$
# \hat{\mathbf{\theta}} = 
# \mathbf{X}^+\, \mathbf{y}
# $$

# **`LinearRegression` 모델**

# 사이킷런의 `LinearRegression` 모델은 특잇값 분해와 무어-펜로즈 유사 역행렬을 이용하여 
# 최적의 $\hat \theta$ 를 계산한다.

# (sec:gradient-descent)=
# ## 경사하강법

# 훈련 세트를 이용한 훈련 과정 중에 가중치 파라미터를 조금씩 반복적으로 조정한다. 
# 이때 비용 함수의 크기를 줄이는 방향으로 조정한다.

# **경사하강법**<font size="2">gradient descent</font>(GD) 이해를 위해 다음 개념들을 충분히 이해하고 있어야 한다.

# **최적 학습 모델**
# 
# 비용 함수를 최소화하는 또는 효용 함수를 최대화하는 파라미터를 사용하는 모델이며,
# 최종적으로 훈련시킬 대상이다.

# **파라미터<font size="2">parameter</font>**
# 
# 선형 회귀 모델에 사용되는 편향과 가중치 파라미터처럼 모델 훈련중에 학습되는 파라미터를 가리킨다.

# **비용 함수<font size="2">cost function</font>**
# 
# 평균 제곱 오차(MSE)처럼 모델이 얼마나 나쁜가를 측정하는 함수다.

# **전역 최솟값<font size="2">global minimum</font>**
# 
# 비용 함수의 전역 최솟값이다. 

# **비용 함수의 그레이디언트 벡터**
# 
# MSE를 비용함수로 사용하는 경우 $\textrm{MSE}(\mathbf{\theta})$ 함수의 $\mathbf{\mathbf{\theta}}$ 에 
# 대한 그레이디언트<font size="2">gradient</font> 벡터를 사용한다.
# 
# $$
# \nabla_\mathbf{\theta} \textrm{MSE}(\mathbf{\theta}) =
# \begin{bmatrix}
#     \frac{\partial}{\partial \mathbf{\theta}_0} \textrm{MSE}(\mathbf{\theta}) \\
#     \frac{\partial}{\partial \mathbf{\theta}_1} \textrm{MSE}(\mathbf{\theta}) \\
#     \vdots \\
#     \frac{\partial}{\partial \mathbf{\theta}_n} \textrm{MSE}(\mathbf{\theta})
# \end{bmatrix}
# $$

# **학습률($\eta$)**
# 
# 훈련 과정에서의 비용함수의 파라미터($\mathbf{\theta}$)를 조정할 때 사용하는 조정 비율이다.

# **에포크<font size="2">epoch</font>**
# 
# 훈련셋에 포함된 모든 데이터를 대상으로 예측값을 계산하는 과정을 가리킨다.

# **허용오차<font size="2">tolerance</font>**
# 
# 비용함수의 값이 허용오차보다 작아지면 훈련을 종료시킨다.

# **배치 크기<font size="2">batch size</font>**
# 
# 파라미터를 업데이트하기 위해, 즉 그레이디언트 벡터를 계산하기 위해 사용되는 훈련 데이터의 개수이다.

# **하이퍼파라미터<font size="2">hyperparameter</font>**
# 
# 학습률, 에포크, 허용오차, 배치 크기 처럼 모델을 지정할 때 사용되는 값을 나타낸다.

# ### 선형 회귀 모델과 경사하강법

# 선형회귀 모델 파라미터를 조정하는 과정을 이용하여 경사하강법의 기본 아이디어를 설명한다.
# 
# 먼저 $\mathrm{MSE}(\mathbf{\theta})$ 는 $\mathbf{\theta}$ 에 대한 2차 함수임에 주의한다.
# 여기서는 $\mathbf{\theta}$ 가 하나의 파라미터로 구성되었다고 가정한다.
# 따라서 $\mathrm{MSE}(\mathbf{\theta})$의 그래프는 포물선이 된다.
# 
# $$
# \mathrm{MSE}(\mathbf{\theta}) =
# \frac 1 m \sum_{i=1}^{m} \big(\mathbf{\theta}^{T}\, \mathbf{x}^{(i)} - y^{(i)}\big)^2
# $$
# 
# $\mathrm{MSE}(\mathbf{\theta})$의 그레이디언트 벡터는 다음과 같다.
# 
# $$
# \nabla_\theta \textrm{MSE}(\theta) = \frac{2}{m}\, \mathbf{X}^T\, (\mathbf{X}\, \theta^T - \mathbf y)
# $$

# 경사하강법은 다음 과정으로 이루어진다. 
# 
# 1. $\mathbf{\theta}$를 임의의 값으로 지정한 후 훈련을 시작한다.
# 
# 1. 아래 단계를 $\textrm{MSE}(\theta)$ 가 허용오차보다 적게 작아지는 단계까지 반복한다.
#     * 지정된 수의 훈련 샘플을 이용한 학습.
#     * $\mathrm{MSE}(\mathbf{\theta})$ 계산.
#     * 이전 $\mathbf{\theta}$에서 $\nabla_\mathbf{\theta} \textrm{MSE}(\mathbf{\theta})$ 와
#         학습률 $\eta$를 곱한 값 빼기.<br><br>
# 
#         $$
#         \theta^{(\text{new})} = \theta^{(\text{old})}\, -\, \eta\cdot \nabla_\theta \textrm{MSE}(\theta^{(\text{old})})
#         $$

# 위 수식은 산에서 가장 경사가 급한 길을 따를 때 가장 빠르게 하산하는 원리와 동일하다.
# 이유는 해당 지점에서 그레이디언트 벡터를 계산하면 정상으로 가는 가장 빠른 길을 안내할 것이기에
# 그 반대방향으로 움직여야 하기 때문이다.

# :::{admonition} 벡터의 방향과 크기
# :class: info
# 
# 모든 벡터는 방향과 크기를 갖는다. 
# 
# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/vector01.png" width="200"/></div>
# 
# 그레이디언트 벡터 또한 방향과 크기에 대한 정보를 제공하며, 
# 그레이디언트가 가리키는 방향의 __반대 방향__으로 움직이면 빠르게 전역 최솟값에 접근한다.
# 
# 이는 아래 그림이 표현하듯이 산에서 가장 경사가 급한 길을 따를 때 가장 빠르게 하산하는 원리와 동일하다.
# 이유는 해당 지점에서 그레이디언트 벡터를 계산하면 정상으로 가는 가장 빠른 길을 안내할 것이기에
# 그 반대방향으로 움직여야 하기 때문이다.
# 
# 아래 그림은 경사하강법을 담당하는 여러 알고리즘을 비교해서 보여준다.
# 
# <table>
#     <tr>
#         <td style="padding:1px">
#             <figure>
#                 <img src="https://ruder.io/content/images/2016/09/contours_evaluation_optimizers.gif" style="width:90%" title="SGD without momentum">
#                 <figcaption>SGD optimization on loss surface contours</figcaption>
#             </figure>
#         </td>
#         <td style="padding:1px">
#             <figure>
#                 <img src="https://ruder.io/content/images/2016/09/saddle_point_evaluation_optimizers.gif" style="width:90%" title="SGD without momentum">
#                 <figcaption>SGD optimization on saddle point</figcaption>
#             </figure>
#         </td>        
#     </tr>
# </table>
# 
# **그림 출처:** [An overview of gradient descent optimization algorithms](https://ruder.io/optimizing-gradient-descent/index.html)
# :::

# **학습률의 중요성**
# 
# 선형 회귀 모델은 적절할 학습률로 훈련될 경우 빠른 시간에 비용 함수의 최솟값에 도달한다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-01.png" width="500"/></div>

# 반면에 학습률이 너무 작거나 크면 비용 함수의 전역 최솟값에 수렴하지 않을 수 있다.
# 
# - 학습률이 너무 작은 경우: 비용 함수가 전역 최소값에 너무 느리게 수렴.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-02.png" width="500"/></div>

# * 학습률이 너무 큰 경우: 비용 함수가 수렴하지 않음.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-03.png" width="500"/></div>

# 선형 회귀가 아닌 경우에는 시작점에 따라 지역 최솟값에 수렴하거나 정체될 수 있음을
# 아래 그림이 잘 보여준다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-04.png" width="500"/></div>

# **특성 스케일링의 중요성**
# 
# 특성들의 스켈일을 통일시키면 보다 빠른 학습이 이루어지는 이유를 
# 아래 그림이 설명한다.
# 
# * 왼편 그림: 두 특성의 스케일이 동일하게 조정된 경우 비용 함수의 최솟값으로 최단거리로 수렴한다.
# * 오른편 그림: 두 특성의 스케일이 다른 경우 비용 함수의 최솟값으로 보다 먼 거리를 지나간다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-04a.png" width="500"/></div>

# ### 경사하강법 종류

# 모델을 지정할 때 지정하는 배치 크기에 따라 세 종류로 나뉜다.

# **참고:** 지정된 배치 크기의 샘플에 대해 예측을 한 후에 경사하강법을 이용하여 파라미터를 조정하는 단계를
# 스텝<font size="2">step</font>이라 하며, 다음이 성립힌다.
# 
#     스텝 크기 = (훈련 샘플 수) / (배치 크기)
# 
# 예를 들어, 훈련 세트의 크기가 1,000이고 배치 크기가 10이면, 에포크 당 100번의 스텝이 실행된다.

# #### 배치 경사하강법

# 에포크마다 그레이디언트를 계산하여 파라미터를 조정한다.
# 즉, 배치의 크기가 전체 훈련셋의 크기와 같고 따라서 스텝의 크기는 1이다.
# 
# 단점으로 훈련 세트가 크면 그레이디언트를 계산하는 데에 많은 시간과 메모리가 필요해지는 문제가 있다. 
# 이와 같은 이유로 인해 사이킷런은 배치 경사하강법을 지원하지 않는다.

# **학습율과 경사하강법의 관계**
# 
# 학습률에 따라 파라미터($\theta$)의 수렴 여부와 속도가 달라진다.
# 최적의 학습률은 그리드 탐색 등을 이용하여 찾아볼 수 있다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-04b.png" width="700"/></div>

# **에포크 수와 허용오차**
# 
# 에포크 수는 크게 설정한 후 허용오차를 지정하여 학습 시간을 제한할 필요가 있다.
# 이유는 포물선의 최솟점에 가까워질 수록 그레이디언트 벡터의 크기가 0에 수렴하기 때문이다.
# 
# 허용오차와 에포크 수는 서로 반비례의 관계이다. 
# 예를 들어, 허용오차를 1/10로 줄이려면 에포크 수를 10배 늘려야한다.

# #### 확률적 경사하강법(SGD)

# 배치 크기가 1이다.
# 즉, 하나의 스텝에 하나의 훈련 셈플에 대한 예측값을 실행한 후에 
# 그 결과를 이용하여 그레이디언트를 계산하고 파라미터를 조정한다.
# 
# 샘플은 무작위로 선택된다.
# 따라서 경우에 따라 하나의 에포크에서 여러 번 선택되거나 전혀 선택되지 않는 샘플이
# 존재할 수도 있지만, 이는 별 문제가 되지 않는다.
# 
# 확률적 경사하강법<font size="2">stochastic graidient descent</font>(SGD)을 이용하면 
# 계산량이 상대적으로 적어 아주 큰 훈련 세트를 다룰 수 있으며,
# 따라서 외부 메모리(out-of-core) 학습에 활용될 수 있다.
# 또한 파라미터 조정이 불안정하게 이뤄질 수 있기 때문에 지역 최솟값에 상대적으로 덜 민감하다.
# 반면에 동일한 이유로 경우에 따라 전역 최솟값에 수렴하지 못하고 주변을 맴돌 수도 있다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-04c.png" width="300"/></div>

# 아래 그림은 처음 20 단계 동안의 SGD 학습 과정을 보여주는데, 모델이 수렴하지 못함을 확인할 수 있다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-04d.png" width="500"/></div>

# **독립 항등 분포**
# 
# 확률적 경사하강법을 적용하려면 훈련셋이 
# 독립 항등 분포<font size="2">independently and identically distributed</font>(iid)를 따르도록 해야 한다.
# 이를 위해 매 에포크마다 훈련 셋을 무작위로 섞는 방법이 일반적으로 사용된다.

# **학습 스케줄<font size="2">learning schedule</font>**
# 
# 요동치는 파라미터를 제어하기 위해 학습률을 학습 과정 동안 천천히 줄어들게 만드는 기법을 의미한다.
# 일반적으로 훈련이 지속될 수록 학습률을 조금씩 줄이며,
# 에포크 수, 훈련 샘플 수, 학습되는 샘플의 인덱스를 이용하여 지정한다. 

# **사이킷런의 `SGDRegressor` 클래스**
# 
# 확률적 경사하강법을 기본적으로 지원한다.
# 
# ```python
# SGDRegressor(max_iter=1000, tol=1e-5, penalty=None, eta0=0.01,
#              n_iter_no_change=100, random_state=42)
# ```
# 
# * `max_iter=1000`: 최대 에포크 수
# * `tol=1e-3`: 허용오차
# * `eta0=0.1`: 학습 스케줄 함수에 사용되는 매개 변수. 일종의 학습률.
# * `penalty=None`: 규제 사용 여부 결정(추후 설명). 여기서는 사용하지 않음.

# #### 미니 배치 경사하강법

# 배치 크기가 2에서 수백 사이로 정해지며, 최적의 배치 크기는 경우에 따라 다르다.
# 배치 크기를 어느 정도 크게 하면 확률적 경사하강법(SGD) 보다 파라미터의 움직임이 덜 불규칙적이 되며,
# 배치 경사하강법보다 빠르게 학습한다.
# 반면에 SGD에 비해 지역 최솟값에 수렴할 위험도가 보다 커진다.

# **경사하강법 비교**
# 
# 배치 GD, 미니 배치 GD, SGD의 순서대로 최적의 파라미터 값에 
# 수렴할 확률이 높다.
# 훈련 시간 또한 동일한 순서대로 오래 걸린다. 

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-05.png" width="500"/></div>

# **선형 회귀 알고리즘 비교**
# 
# | 알고리즘   | 많은 샘플 수 | 외부 메모리 학습 | 많은 특성 수 | 하이퍼 파라미터 수 | 스케일 조정 | 사이킷런 지원 |
# |:--------:|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
# | 정규방정식  | 빠름       | 지원 안됨      |  느림        | 0          | 불필요    | 지원 없음      |
# | SVD      | 빠름       | 지원 안됨      |  느림        | 0          | 불필요     | LinearRegression     |
# | 배치 GD   | 느림       | 지원 안됨      |  빠름        | 2          | 필요      | (?)      |
# | SGD      | 빠름       | 지원          |  빠름        | >= 2       | 필요      | SGDRegressor |
# | 미니배치 GD | 빠름       | 지원         |  빠름        | >=2        | 필요      | 지원 없음      |

# **참고:** 심층 신경망을 지원하는 텐서플로우<font size="2">Tensorflow</font>는 
# 기본적으로 미니 배치 경사하강법을 지원한다.

# (sec:poly_reg)=
# ## 다항 회귀

# 비선형 데이터를 선형 회귀를 이용하여 학습하는 기법을
# **다항 회귀**<font size="2">polynomial regression</font>라 한다.
# 이때 다항식을 이용하여 새로운 특성을 생성하는 아이디어를 사용한다.

# **2차 함수 모델를 따르는 데이터셋에 선형 회귀 모델 적용 결과**
# 
# 아래 그림은 2차 함수의 그래프 형식으로 분포된 데이터셋을 선형 회귀 모델로 학습시킨 결과를 보여준다.
# 
# $$\hat y = \theta_0 + \theta_1\, x_1$$

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-06.png" width="500"/></div>

# **2차 함수 모델를 따르는 데이터셋에 2차 다항식 모델 적용 결과**
# 
# 반면에 아래 그림은 $x_1^2$ 에 해당하는 특성 $x_2$ 를 새로이 추가한 후에
# 선형 회귀 모델을 학습시킨 결과를 보여준다.
# 
# $$\hat y = \theta_0 + \theta_1\, x_1 + \theta_2\, x_{2}$$

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-07.png" width="500"/></div>

# **사이킷런의 `PolynomialFeatures` 변환기**
# 
# 활용하고자 하는 다항식에 포함되어야 하는 항목에 해당하는 특성들을 생성하는 변환기이다.
# 
# ```python
# PolynomialFeatures(degree=d, include_bias=False)
# ```
# `degree=d`는 몇 차 다항식을 활용할지 지정하는 하이퍼파라미터이다. 

# :::{prf:example} 3차 다항 회귀
# :label: exp:3rd_poly_reg
# 
# 기존에 두 개의 $x_1, x_2$ 두 개의 특성을 갖는 데이터셋에 대해
# 3차 다항식 모델을 훈련시키고자 하면 $d=3$으로 설정한다.
# 그러면 $x_1, x_2$ 을 이용한 2차, 3차 다항식에 포함될 항목을 새로운 특성으로 추가해야 한다.
# 이는 $(x_1+x_2)^2$과 $(x_1+x_2)^3$의 항목에 해당하는 다음 7개의 특성을 추가해야 함을 의미한다.
# 
# $$x_1^2,\,\, x_1 x_2,\,\, x_2^2,\,\, x_1^3,\,\, x_1^2 x_2,\,\, x_1 x_2^2,\,\, x_2^3$$
# :::

# ## 학습 곡선

# 다항 회귀 모델의 차수에 따라 훈련된 모델이 훈련 세트에 과소 또는 과대 적합할 수 있다.
# 아래 그림이 보여주듯이 선형 모델은 과소 적합되어 있는 반면에 
# 300차 다항 회귀 모델 과대 적합 되어 있다. 
# 그리고 2차 다항 회귀 모델의 일반화 성능이 가장 좋다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-08.png" width="500"/></div>

# **교차 검증 vs. 학습 곡선**
# 
# 하지만 일반적으로 몇 차 다항 회귀가 가장 좋은지 미리 알 수 없다. 
# 따라서 다양한 모델을 대상으로 교차 검증을 진행하여 과소 또는 과대 적합 모델을 구별해야 한다.
# 
# * 과소 적합: 훈련 세트와 교차 검증 점수 모두 낮은 경우
# * 과대 적합: 훈련 세트에 대한 검증은 우수하지만 교차 검증 점수가 낮은 경우
# 
# 다른 검증 방법은 **학습 곡선**<font size='2'>learning curve</font>을 잘 살펴보는 것이다.
# 학습 곡선은 훈련 세트와 검증 세트에 대한 모델 성능을 비교하는 그래프이며,
# 학습 곡선의 모양에 따라 과소 적합 또는 과대 적합 여부를 판정할 수 있다.
# 
# 사이킷런의 `learning_curve()` 함수를 이용하여 학습 곡선을 그릴 수 있다.
# 
# * x 축: 훈련셋 크기. 전체 훈련셋의 10%에서 출발하여 훈련셋 전체를 대상으로 할 때까지 
#     훈련셋의 크기를 키워가며 교차 검증 진행.
# * y 축: 교차 검증을 통해 확인된 훈련셋 및 검증셋 대상 RMSE(평균 제곱근 오차).

# **과소 적합 모델의 학습 곡선 특징**
# 
# * 훈련셋(빨강)에 대한 성능: 훈련 세트가 커지면서 RMSE 증가하지만 
#     훈련 세트가 어느 정도 커지면 거의 불변.
# 
# * 검증셋(파랑)에 대한 성능: 검증 세트에 대한 성능이 훈련 세트에 대한 성능과 거의 비슷해짐.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-09.png" width="500"/></div>

# **과대 적합 모델의 학습 곡선 특징**
# 
# * 훈련셋(빨강)에 대한 성능: 훈련 데이터에 대한 평균 제곱근 오차가 매우 낮음.
# * 검증셋(파랑)에 대한 성능: 훈련 데이터에 대한 성능과 차이가 어느 정도 이상 벌어짐.
# * 과대 적합 모델 개선법: 두 그래프가 맞닿을 때까지 훈련 데이터 추가. 
#     하지만 일반적으로 더 많은 훈련 데이터를 구하는 일이 매우 어렵거나 불가능할 수 있음.
#     아니면 모델에 규제를 가할 수 있음.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-10.png" width="500"/></div>

# **모델 일반화 오차의 종류**
# 
# 훈련 후에 새로운 데이터 대한 예측에서 발생하는 오차를 가리키며 세 종류의 오차가 있다.
# 
# - 편향: 실제로는 2차원 모델인데 1차원 모델을 사용하는 경우처럼 잘못된 가정으로 인해 발생한다.
#     과소 적합이 발생할 가능성이 매우 높다.
# 
# - 분산: 모델이 훈련 데이터에 민감하게 반응하는 정도를 가리킨다.
#     고차 다항 회귀 모델일 수록 분산이 높아질 수 있다.
#     일반적으로 **자유도**<font size='2'>degree of freedom</font>가 높은 모델일 수록 분산이 커지며,
#     과대 적합이 발생할 가능성도 매우 높다.
# - 축소 불가능 오차: 잡음(noise) 등 데이터 자체의 한계로 인해 발생한다.
#     잡음 등을 제거해야 오차를 줄일 수 있다.

# :::{prf:example} 편향-분산 트레이드오프
# :label: exp:bias_variance
# 
# 복잡한 모델일 수록 편향을 줄어들지만 분산을 커진다.
#  :::

# ## 규제 사용 선형 모델

# 훈련 중에 과소 적합이 발생하면 보다 복잡한 모델을 선택해야 한다.
# 반면에 과대 적합이 발생할 경우 먼저 모델에 규제를 가해 과대 적합을 방지하거나
# 아니면 최소한 과대 적합이 최대한 늦게 발생하도록 유도해야 한다. 

# 모델 규제는 보통 모델의 자유도를 제한하는 방식으로 이루어진다. 
# **자유도**<font size="2">degree of freedom</font>는 모델 결정에 영향을 주는 요소들의 개수이다.
# 예를 들어 선형 회귀의 경우에는 특성 수가 자유도를 결정하며,
# 다항 회귀의 경우엔 차수도 자유도에 기여한다.
# 
# 선형 회귀 모델에 대한 **규제**<font size='2'>regularization</font>는 가중치를 제한하는 방식으로 이루어지며,
# 방식에 따라 다음 세 가지 선형 회귀 모델이 지정된다.
# 
# * 릿지 회귀
# * 라쏘 회귀
# * 엘라스틱 넷

# :::{admonition} 주의
# :class: warning
# 
# 규제는 훈련 과정에만 사용된다. 테스트 과정에는 다른 기준으로 성능을 평가한다.
# 
# * 훈련 과정: 비용 최소화 목표
# * 테스트 과정: 최종 목표에 따른 성능 평가. 
#     예를 들어, 분류기의 경우 재현율/정밀도 기준으로 모델의 성능을 평가한다.
# :::

# ### 릿지 회귀<font size='2'>Ridge Regression</font>

# 다음 비용 함수를 사용하며,
# 특성 스케일링을 해야 규제의 성능이 좋아진다.
# 
# $$J(\theta) = \textrm{MSE}(\theta) + \alpha \sum_{i=1}^{n}\theta_i^2$$
# 
# * $\alpha$(알파)는 규제의 강도를 지정한다. 
#     $\alpha=0$ 이면 규제가 전혀 없는 기본 선형 회귀이다.
# 
# * $\alpha$ 가 커질 수록 가중치의 역할이 줄어든다.
#     왜냐하면 비용을 줄이기 위해 보다 작은 가중치를 선호하는 방향으로 훈련되기 때문이다.
# 
# * $\theta_0$ 는 규제하지 않는다.

# 아래 그림은 릿지 규제를 적용한 적용한 6 개의 경우를 보여준다.
# 
# - 왼편: 선형 회귀 모델에 세 개의 $\alpha$ 값 적용.
# - 오른편: 10차 다항 회귀 모델에 세 개의 $\alpha$ 값 적용.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/ridge01.png" width="600"/></div>

# :::{admonition} 릿지 회귀의 정규 방정식
# :class: info
# 
# $A$ 가 `(n+1)x(n+1)` 모양의 단위 행렬<font size='2'>identity matrix</font>일 때 다음이 성립한다.
# 
# $$
# \hat{\mathbf{\theta}} = 
# (\mathbf{X}^T\, \mathbf{X} + \alpha A)^{-1}\, \mathbf{X}^T\, \mathbf{y}
# $$
# :::

# ### 라쏘 회귀<font size='2'>Lasso Regression</font>

# 다음 비용 함수를 사용한다.
# 
# $$J(\theta) = \textrm{MSE}(\theta) + \alpha \, \sum_{i=1}^{n}\mid \theta_i\mid$$
# 
# * 별로 중요하지 않은 특성에 대해 $\theta_i$가 0에 빠르게 수렴하도록 훈련 중에 유도된다.
#     이유는 $\mid \theta_i \mid$ 의 미분값이 1또는 -1 이기에 상대적으로 큰 값이기에
#     파라미터 업데이크 과정에서 보다 작은 $\mid \theta_i \mid$ 가 보다 빠르게 0에 수렴하기 때문이다.
#    
# * $\alpha$ 와 $\theta_0$ 에 대한 설명은 릿지 회귀의 경우와 동일하다.

# 아래 그림은 라쏘 규제를 적용한 적용한 6 개의 경우를 보여준다.
# 
# - 왼편: 선형 회귀 모델에 세 개의 $\alpha$ 값 적용.
# - 오른편: 10차 다항 회귀 모델에 세 개의 $\alpha$ 값 적용.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/lasso01.png" width="600"/></div>

# :::{admonition} 주의 사항
# :class: warning
# 
# 라쏘 회귀는 정규 방정식을 지원하지 않는다.
# :::

# ### 엘라스틱 넷<font size='2'>Elastic Net</font>

# 릿지 회귀와 라쏘 회귀를 절충한 모델이며 다음 비용 함수를 사용한다.
# $r$ 은 릿지 규제와 라쏘 규제의 사용 비율이다. 
# 단, 규제 강도를 의미하는 `\alpha` 가 각 규제에 가해지는 정도가 다름에 주의한다.
# 
# $$
# J(\theta) = 
# \textrm{MSE}(\theta) + 
# r\cdot \bigg (2 \alpha \, \sum_{i=1}^{n}\mid\theta_i\mid \bigg) + 
# (1-r)\cdot \bigg (\frac{\alpha}{m}\, \sum_{i=1}^{n}\theta_i^2 \bigg )
# $$

# :::{admonition} 규제 선택
# :class: info
# 
# 약간이라도 규제를 사용해야 하며, 일반적으로 릿지 회귀가 추천된다.
# 반면에 유용한 속성이 그렇게 많지 않다고 판단되는 경우엔 라쏘 회귀 또는 엘라스틱 넷이 추천된다.
# 
# 하지만 특성 수가 훈련 샘플 수보다 크거나 특성 몇 개가 강하게 연관되어 있는 경우엔 엘라스틱 넷을
# 사용해야 한다.
# :::

# (sec:early-stopping)=
# ### 조기 종료

# **조기 종료**<font size='2'>Early Stopping</font>는 
# 모델이 훈련셋에 과대 적합하는 것을 방지하기 위해 훈련을 적절한 시기에 중단시키는 기법이며,
# 검증 데이터에 대한 손실이 줄어들다가 다시 커지는 순간 훈련을 종료한다. 
# 
# 확률적 경사하강법, 미니 배치 경사하강법에서는 손실 곡선이 보다 많이 진동하기에
# 검증 손실이 언제 최소가 되었는지 알기 어렵다.
# 따라서 한동안 최솟값보다 높게 유지될 때 훈련을 멈추고 기억해둔 최적의 모델로
# 되돌린다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-11.png" width="500"/></div>

# ## 로지스틱 회귀

# 회귀 모델을 분류 모델로 활용할 수 있다. 
# 
# * 이진 분류: 로지스틱 회귀
# * 다중 클래스 분류: 소프트맥스 회귀

# ### 확률 추정

# 선형 회귀 모델이 예측한 값에 **시그모이드**<font size='2'>sigmoid</font> 함수를
# 적용하여 0과 1 사이의 값, 즉 양성일 **확률** $\hat p$ 로 지정한다.
# 
# $$
# \hat p = h_\theta(\mathbf{x}) = \sigma(\mathbf{\theta}^T \, \mathbf{x})
# = \sigma(\theta_0 + \theta_1\, x_1 + \cdots + \theta_n\, x_n)
# $$

# **시그모이드 함수**
# 
# $$\sigma(t) = \frac{1}{1 + \exp(-t)}$$

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-12.png" width="500"/></div>

# 로지스틱 회귀 모델의 **예측값**은 다음과 같다.
# 
# $$
# \hat y = 
# \begin{cases}
# 0 & \text{if}\,\, \hat p < 0.5 \\[1ex]
# 1 & \text{if}\,\, \hat p \ge 0.5
# \end{cases}
# $$

# 즉, 다음이 성립한다.
# 
# * 양성: $\theta_0 + \theta_1\, x_1 + \cdots + \theta_n\, x_n \ge 0$
# 
# * 음성: $\theta_0 + \theta_1\, x_1 + \cdots + \theta_n\, x_n < 0$

# ### 훈련과 비용함수

# 로지스틱 회귀 모델은 양성 샘플에 대해서는 1에 가까운 확률값을,
# 음성 샘플에 대해서는 0에 가까운 확률값을 내도록 훈련한다.
# 각 샘플에 대한 비용은 다음과 같다.
# 
# $$
# c(\theta) = 
# \begin{cases}
# -\log(\,\hat p\,) & \text{$y=1$ 인 경우}\\
# -\log(\,1 - \hat p\,) & \text{$y=0$ 인 경우}
# \end{cases}
# $$
# 
# 양성 샘플에 대해 0에 가까운 값을 예측하거나,
# 음성 샘플에 대해 1에 가까운 값을 예측하면 
# 위 비용 함수의 값이 무한히 커진다.
# 
# 모델 훈련은 따라서 전체 훈련셋에 대한 다음 
# **로그 손실**<font size='2'>log loss</font> 함수는 다음과 같다.
# 
# $$
# J(\theta) = 
# - \frac{1}{m}\, \sum_{i=1}^{m}\, [y^{(i)}\, \log(\,\hat p^{(i)}\,) + (1-y^{(i)})\, \log(\,1 - \hat p^{(i)}\,)]
# $$

# :::{admonition} 로그 손실 함수 이해
# :class: info
# 
# $c(\theta)$ 는 틀린 예측을 하면 손실값이 매우 커진다.
# 
# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-12-10a.png" width="500"/></div>
# 
# 훈련셋이 가우시안 분포를 따른다는 전제하에 로그 손실 함수를 최소화하면 
# **최대 우도**<font size='2'>maximal likelihood</font>를 갖는 최적의 모델을 얻을 수 있다는 사실은
# 수학적으로 증명되었다.
# 상세 내용은 [앤드류 응(Andrew Ng) 교수의 Stanford CS229](https://www.youtube.com/watch?v=jGwO_UgTS7I&list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU) 강의에서 들을 수 있다.
# :::

# 최적의 $\theta$ 를 계산하는 정규 방정식은 하지 않는다.
# 하지만 다행히도 경사하강법은 적용할 수 있으며,
# 선형 회귀의 경우처럼 적절한 학습률을 사용하면 언제나 최소 비용에 수렴하도록
# 파라미터가 훈련된다.
# 
# 참고로 로그 손실 함수의 그레이디이언트 벡터는 선형 회귀의 그것과 매우 유사하며,
# 다음 편도 함수들로 이루어진다.
# 
# $$
# \dfrac{\partial}{\partial \theta_j} J(\boldsymbol{\theta}) = \dfrac{1}{m}\sum\limits_{i=1}^{m}\left(\mathbf{\sigma(\boldsymbol{\theta}}^T \mathbf{x}^{(i)}) - y^{(i)}\right)\, x_j^{(i)}
# $$

# ### 결정 경계

# 붓꽃 데이터셋을 이용하여 로지스틱 회귀의 사용법을 살펴 본다. 
# 하나의 붓꽃 샘플은 꽃받침<font size='2'>sepal</font>의 길이와 너비, 
# 꽃입<font size='2'>petal</font>의 길이와 너비 등 총 4개의 특성으로 
# 이루어진다. 
# 
# 타깃값은 0, 1, 2 중에 하나이며 각 숫자는 다음 세 개의 품종을 가리킨다. 
# 
# * 0: Iris-Setosa(세토사)
# * 1: Iris-Versicolor(버시컬러)
# * 2: Iris-Virginica(버지니카)

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/iris01.png" width="600"/></div>

# **버지니카 품종 감지기**
# 
# 로지스틱 회귀 모델을 이용하여 아이리스 데이터셋을 대상으로 버지니카 품종을 감지하는
# 이진 분류기를 다음과 같이 훈련시킨다.
# 단, 문제를 간단하기 만들기 위해 꽃잎의 너비 속성 하나만 이용한다. 
# 
# ```python
# X = iris.data[["petal width (cm)"]].values
# y = iris.target_names[iris.target] == 'virginica'
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
# 
# log_reg = LogisticRegression(random_state=42)
# log_reg.fit(X_train, y_train)
# ```
# 
# 훈련 결과 꽃잎의 넙가 약 1.65cm 보다 큰 경우 버지니카 품종일 가능성이 높아짐이 확인된다.
# 즉, 버지니카 품좀 감지기의 
# **결정 경계**<font size='2'>decision boundary</font>는 꽃잎 넙 기준으로 약 1.65cm 이다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/iris02.png" width="700"/></div>

# 아래 그림은 꽃잎의 너비와 길이 두 속성을 이용한 버지니카 품종 감지기가 찾은 
# 결정 경계(검정 파선)를 보여준다. 
# 반면에 다양한 색상의 직선은 버지니카 품종일 가능성을 보여주는 영역을 표시한다. 

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-15.png" width="700"/></div>

# **로지스틱 회귀 규제**
# 
# `LogisticRegression` 모델의 하이퍼파라미터 `penalty` 와 `C` 를 이용하여 규제와 규제의 강도를 지정한다. 
# 
# * `penalty`: `l1`(라쏘 규제), `l2`(릿지 규제), `elasticnet`(엘라스틱 넷) 방식 중 하나 선택하며,
#     기본값은 `l2`, 즉, 릿지 규제를 기본으로 적용한다.
# 
# * `C`: 릿지 또는 라쏘 규제 정도를 지정하는 $\alpha$의 역수에 해당한다. 
#     따라서 0에 가까울 수록 강한 규제를 의미한다.

# (sec:softmax-regression)=
# ### 소프트맥스 회귀

# 로지스틱 회귀 모델을 일반화하여 다중 클래스 분류를 지원하도록 만든 모델이
# **소프트맥스 회귀**<font size='2'>Softmax Regression</font>이며, 
# **다항 로지스틱 회귀** 라고도 불린다.

# **클래스별 확률 예측**
# 
# 샘플 $\mathbf x$가 주어졌을 때 각각의 분류 클래스 $k$ 에 대한 점수 $s_k(\mathbf x)$를
# 선형 회귀 방식으로 계산한다.
# 
# $$
# s_k(\mathbf{x}) = \theta_0^{(k)} + \theta_1^{(k)} x_1 + \cdots + \theta_n^{(k)} x_n
# $$    
# 
# 이는 $k\, (n+1)$ 개의 파라미터를 학습시켜야 함을 의미한다.
# 위 식에서 $\theta_i^{(k)}$ 는 분류 클래스 $k$에 대해 필요한 $i$ 번째 속성을 
# 대상으로 파라미터를 가리킨다.
# 
# 예를 들어, 붓꽃 데이터를 대상으로 하는 경우 최대 15개의 파라미터를 훈련시켜야 한다.
# 
# $$
# \Theta = 
# \begin{bmatrix}
# \theta_0^{(0)} & \theta_1^{(0)} & \theta_2^{(0)} & \theta_3^{(0)} & \theta_4^{(0)}\\
# \theta_0^{(1)} & \theta_1^{(1)} & \theta_2^{(1)} & \theta_3^{(1)} & \theta_4^{(1)}\\
# \theta_0^{(2)} & \theta_1^{(2)} & \theta_2^{(2)} & \theta_3^{(2)} & \theta_4^{(2)}
# \end{bmatrix}
# $$
# 
# 이제 다음 **소프트맥스** 함수를 이용하여 클래스 $k$에 속할 확률 $\hat p_k$ 를 계산한다.
# 단, $K$ 는 클래스의 개수를 나타낸다.
# 
# $$
# \hat p_k = 
# \frac{\exp(s_k(\mathbf x))}{\sum_{j=1}^{K}\exp(s_j(\mathbf x))}
# $$
# 
# 소프트맥스 회귀 모델은 각 샘플에 대해 추정 확률이 가장 높은 클래스를 선택한다. 
# 
# $$
# \hat y = 
# \mathrm{argmax}_k s_k(\mathbf x)
# $$

# :::{admonition} 소프트맥스 회귀와 다중 출력 분류
# :class: tip
# 
# 소프트맥스 회귀는 다중 출력<font size='2'>multioutput</font> 분류를 지원하지 않는다.
# 예를 들어, 하나의 사진에서 여러 사람의 얼굴을 인식하는 데에 사용할 수 없다.
# :::

# **소프트맥스 회귀의 비용 함수**
# 
# 각 분류 클래스 $k$에 대한 적절한 가중치 벡터 $\theta_k$를 
# 경사하강법을 이용하여 업데이트 한다.
# 이를 위해 **크로스 엔트로피**<font size='2'>cross entropy</font>를 비용 함수로 사용한다.
# 
# $$
# J(\Theta) = 
# - \frac{1}{m}\, \sum_{i=1}^{m}\sum_{k=1}^{K} y^{(i)}_k\, \log\big( \hat{p}_k^{(i)}\big)
# $$
# 
# 위 식에서 $y^{(i)}_k$ 는 타깃 확률값을 가리키며, 0 또는 1 중에 하나의 값을 갖는다. 
# $K=2$이면 로지스틱 회귀의 로그 손실 함수와 정확하게 일치한다.
# 
# 크로스 엔트로피는 주어진 샘플의 타깃 클래스를 제대로 예측하지 못하는 경우 높은 값을 갖는다.
# 크로스 엔트로피 개념은 정보 이론에서 유래하며, 
# 자세한 설명은 오렐리앙 제롱의 동영상
# ["A Short Introduction to Entropy, Cross-Entropy and KL-Divergence"](https://www.youtube.com/watch?v=ErfnhcEV1O8)를
# 참고하기 바란다.

# **붓꽃 데이터 다중 클래스 분류**
# 
# 사이킷런의 `LogisticRegression` 예측기를 활용한다.
# 기본값 `solver=lbfgs` 사용하면 모델이 알아서 다중 클래스 분류를 훈련한다.
# 아래 코드는 꽃잎의 길이와 너비 두 특성을 이용하여 
# 세토사, 버시컬러, 버지니카 클래스를 선택하는 모델을 훈련시킨다.
# 
# ```python
# X = iris.data[["petal length (cm)", "petal width (cm)"]].values
# y = iris["target"]
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
# 
# softmax_reg = LogisticRegression(C=30, random_state=42)
# softmax_reg.fit(X_train, y_train)
# ```
# 
# 아래 그림은 붓꽃 꽃잎의 너비와 길이를 기준으로 세 개의 품종을 색까로 구분하는 결정 경계를 보여준다. 
# 다양한 색상의 곡선은 버시컬러 품종에 속할 확률의 영력을 보여준다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/handson-ml3/master/jupyter-book/imgs/ch04/homl04-16.png" width="700"/></div>

# ## 연습문제

# 참고: [(실습) 모델 훈련](https://colab.research.google.com/github/codingalzi/handson-ml3/blob/master/practices/practice_training_models.ipynb)
