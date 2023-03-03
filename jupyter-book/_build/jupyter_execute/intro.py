#!/usr/bin/env python
# coding: utf-8

# # 강의 소개

# **감사의 글**
# 
# 여기서 소개하는 내용은 오렐리앙 제롱의 
# [Hands-on Machine Learning (3판)](https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/)의 
# [주피터 노트북](https://github.com/ageron/handson-ml3)을 활용한 머신러닝 기초 강의노트입니다. 

# **머시러닝/딥러닝**

# 머신러닝/딥러닝 기술이 획기적으로 발전하면서 데이터 분석 및 인공지능 관련 연구의 
# 중요성이 사회, 경제, 산업의 거의 모든 분야에 지대한 영향을 미치고 있으며,
# 앞으로 그런 경향이 더욱 강화될 것으로 기대된다.
# 
# 본 강의는 머신러닝/딥러닝 기본 아이디어와 다양한 활용법을 실전 예제와 함께 전달한다. 
# 머신러닝/딥러닝 학습을 위해 아래 분야의 기초지식이 요구되지만 여기서는 필요한 최소의 내용만 다룬다.
# 
# - 파이썬 프로그래밍
# - 파이썬 데이터분석
# - 선형대수, 확률과통계

# **인공지능, 머신러닝, 딥러닝, 데이터 과학**

# 인공지능, 머신러닝, 딥러닝을 간략하게 정의하면 다음과 같다.
# 
# * 인공지능: 사고<font size='2'>thinking</font>, 학습<font size='2'>learning</font> 등 
#     인간의 지적능력을 컴퓨터가 모방하는 기술 또는 관련 연구
# * 머신러닝: 컴퓨터가 데이터로부터 스스로 정보를 추출하도록 하는 기법 또는 관련 연구
# * 딥러닝: 심층 신경망을 이용하여 복잡한 비선형 문제를 해결하는 머신러닝 기법 또는 관련 연구

# 역사적 관점에서 바라본 인공지능, 머신러닝, 딥러닝의 관계는 다음과 같다.
# 
# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/datapy/master/jupyter-book//images/ai-ml-relation2.png" style="width:600px;"></div>
# 
# <p><div style="text-align: center">&lt;그림 출처: <a href="https://blogs.nvidia.com/blog/2016/07/29/whats-difference-artificial-intelligence-machine-learning-deep-learning-ai/">NVIDIA 블로그</a>&gt;</div></p>

# 데이터 과학과 인공지능, 머신러닝, 딥러닝의 관계는 아래 그림으로 설명된다.
# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/datapy/master/jupyter-book/images/ai-ml-relation.png" style="width:500px;"></div>
# 
# <p><div style="text-align: center">&lt;그림 출처: <a href="http://www.kyobobook.co.kr/readIT/readITColumnView.laf?thmId=00198&sntnId=14142">교보문고: 에이지 오브 머신러닝</a>&gt;</div></p>

# **파이썬 프로그래밍 언어**

# 프로그래밍 실습에 사용되는 파이썬<font size='2'>Python</font>은 현재 데이터 분석 및 머신러닝 분야에서 
# 가장 많이 사용되는 프로그래밍언어이다.
# 
# 또한 수 많은 프로그래밍언어 중에서 현재 가장 많이 사람들 사이에서 회자되고 있다. 
# 아래 사진은 2023년 2월 기준 인터넷 검색 엔진에서 언급된 빈도를 측정한
# [TIOBE Index](https://www.tiobe.com/tiobe-index/)의 상위 결과를 보여준다.
# 
# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/datapy/master/jupyter-book/images/tiobe-index.jpg" style="width:750px"></div>

# **파이썬 주요 라이브러리**

# 파이썬이 데이터 과학 분야에서 인기가 높은 이유는 다음과 같다.
# 
# * 범용 프로그래밍언어
# * R, 매트랩, SQL, 엑셀 등 특정 분야에서 유용하게 사용되는 언어들의 기능 지원
# * 수치 해석, 통계, 확률 등에 유용한 라이브러리 제공
#     * [싸이파이<font size='2'>SciPy</font>](https://scipy.org)
#     * [스탯츠모델즈<font size='2'>statsmodels</font>](https://www.statsmodels.org/stable/index.html)
# * 데이터 처리, 시각화 등에 필요한 라이브러리 제공
#     * [넘파이<font size='2'>NumPy</font>](https://numpy.org)
#     * [판다스<font size='2'>Pandas</font>](https://pandas.pydata.org)
#     * [맷플롯립<font size='2'>Matplotlib</font>](https://matplotlib.org)
# * 머신러닝, 데이터 분석 등에 활용될 수 있는 라이브러리 및 도구의 지속적 개발
#     * [사이킷런<font size='2'>scikit-learn</font>](https://scikit-learn.org/)
#     * [텐서플로우<font size='2'>TensorFlow</font>](https://www.tensorflow.org/)
#     * [케라스<font size='2'>Keras</font>](https://keras.io/)
#     * [파이토치<font size='2'>PyTorch</font>](https://keras.io/)    

# [Stack Overflow 개발자 설문조사 2022](https://survey.stackoverflow.co/2022/)에 따르면
# 개발자로서 가장 배우고 싶어하는 라이브러리로 파이썬의 데이터과학 관련 라이브러리가
# 높은 우선 순위를 갖는다.
# 여기서는 머신러닝의 기본 모델과 훈련을 지원하는 사이킷런<font size='2'>scikit-learn</font>을 주로 다룬다.

# <div align="center"><img src="https://raw.githubusercontent.com/codingalzi/datapy/master/jupyter-book/images/wanted_languages.jpg" style="width:450px"></div>
