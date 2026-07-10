# Retail Operations Analytics

A portfolio project focused on retail demand forecasting, replenishment planning, and inventory allocation using the M5 retail dataset.

## Project Overview

Retail operations teams must balance product availability with inventory cost. Forecasting too low can contribute to stockouts and lost sales, while forecasting too high can create excess inventory and inefficient allocation.

This project builds an end-to-end retail analytics workflow that begins with category-level demand forecasting and later extends toward SKU-store forecasting, replenishment logic, and allocation decisions.

The project is intentionally developed in stages so that each modeling decision can be compared against a simple and defensible benchmark.

## Business Problem

The core business question is:

> How can historical POS demand be translated into reliable forecasts and operational replenishment decisions?

The project addresses several related questions:

- How does demand behavior differ across retail categories?
- Which simple forecasting methods provide the strongest baseline?
- How much do seasonality, holidays, and events affect forecast accuracy?
- Which categories are easier or harder to forecast?
- How can forecast outputs support replenishment and allocation decisions?
- How should forecasting methods change when moving from category-level demand to SKU-store demand?

## Project Objectives

1. Prepare reusable retail demand datasets.
2. Explore category-level trends, seasonality, volatility, and calendar effects.
3. Build baseline forecasts for `FOODS`, `HOBBIES`, and `HOUSEHOLD`.
4. Evaluate forecasts using MAE, WAPE, and bias.
5. Compare simple baselines against statistical and feature-aware models.
6. Extend the workflow to SKU-store forecasting.
7. Translate forecasts into replenishment and allocation logic.

## Dataset

This project uses the M5 Forecasting dataset, which contains historical daily unit sales from Walmart stores across multiple states and product categories.

The dataset includes:

- Daily unit sales
- Product hierarchy
- Store and state hierarchy
- Calendar events
- SNAP indicators
- Selling prices

The first modeling stage uses processed category-level datasets created during data preparation and exploratory analysis.
