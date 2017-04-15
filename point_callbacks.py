import ExchangeRate
callbacks = {}
#12 13
def f12(message_sender):
    message_sender("1$ = "+ExchangeRate.dollar +"RUB")
def f13(message_sender):
    message_sender("1€ = "+ExchangeRate.euro +"RUB")

callbacks[12] = f12
callbacks[13] = f13

