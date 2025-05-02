def assign_strategy(metrics):
    # Conservative: Low volatility, stable moving averages
    if metrics['volatility'] < 0.2 and metrics['ma_30'] > metrics['ma_180'] > metrics['ma_365']:
        return 'Conservative'
    
    # Moderately Aggressive: Moderate volatility and decent growth
    elif 0.2 <= metrics['volatility'] < 0.4 and metrics['ma_30'] > metrics['ma_180']:
        return 'Moderately Aggressive'
    
    # Aggressive: High volatility, growth-oriented
    else:
        return 'Aggressive'
