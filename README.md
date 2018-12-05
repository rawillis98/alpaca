# alpaca
Implemented a strategy based on research paper (linked in readme) to paper trade on alpaca.markets

Link to paper with original strategy: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2604248

Strategy: check if wood outperformed gold by comparing returns over a certain period (see fs variable in main.py for pandas resampling frequency). If wood outperformed gold, the market should theoretically perform well over the next period; if gold outperformed wood, the market might drop over the next period. Buy and sell a leveraged S&P 500 ETF accordingly.

main.py is scheduled with crontab to run on an Ubuntu free tier Google Cloud Platform server 

helper.py contains helper functions such as a function to push a pushbullet notification about what the program did
