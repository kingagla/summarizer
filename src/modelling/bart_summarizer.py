class BARTAbstractiveSummarizer:
    """
    Abstractive summary creator - uses BART pre-trained model to create abstractive summary
    """

    def __init__(self, article, config, tokenizer, model):
        # article
        self._title = article['title']
        self._text = article['text']

        # define model
        self.config = config
        self.tokenizer = tokenizer
        self.model = model

    @property
    def title(self):
        return self._title

    @property
    def text(self):
        return self._text

    def create_summary(self):
        inputs = self.tokenizer([self._text], max_length=1024, return_tensors='pt')
        summary_ids = self.model.generate(inputs['input_ids'], num_beams=4, max_length=60, early_stopping=True)
        return [self.tokenizer.decode(g, skip_special_tokens=True,
                                      clean_up_tokenization_spaces=False) for g in summary_ids][0]
