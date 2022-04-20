import logging


class PredictionObject:
    def __init__(self, model_to_explain, arguments, **kwargs):
        self.model_to_explain = model_to_explain
        self.model_to_explain_name = arguments.model_to_explain_name

    def predict_proba(self, data):
        if self.model_to_explain_name == 'Test':
            prediction = self.model_to_explain(data)

        # add here you code so your model_to_explain can make a prediction
        else:
            raise AssertionError(f'Specified model_to_explain >>{self.model_to_explain_name}<<is unknown')
        return prediction
