# LAB4.0

Суть лабораторной работы в исследовании влияния различных политик изменения темпа обучения на процесс обучения нейронной сети MobileNetV2[1] в контексте решения задачи классификации с использованием набора данных Intel Image Classification

## 1) Пошаговое затухание

   initial_lrate = 0.0001
   
   drop = 0.5         
   epochs_drop = 15.0  
    
![Image alt](https://github.com/PavelPoukh/LAB4.0/blob/master/graphs/1.png)

## 2) Экспоненциальное затухание


![Image alt](https://github.com/PavelPoukh/LAB4.0/blob/master/graphs/2.png)

## 3) Пошаговое затухание с предварительным разогревом
 

![Image alt](https://github.com/PavelPoukh/LAB4.0/blob/master/graphs/3.png)

## 4) Экспоненциальное затухание с предвоарительным разогревом


   
![Image alt](https://github.com/PavelPoukh/LAB4.0/blob/master/graphs/4.png)
