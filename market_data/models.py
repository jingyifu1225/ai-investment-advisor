from django.db import models


current_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
daily_high = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
daily_low = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
daily_open = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
daily_volume = models.BigIntegerField(null=True, blank=True)
last_updated = models.DateTimeField(auto_now=True)


@property
def current_value(self):
    if self.current_price is not None:
        return self.current_price * self.quantity
    return self.purchase_price * self.quantity


@property
def profit_loss(self):
    if self.current_price is not None:
        return (self.current_price - self.purchase_price) * self.quantity
    return 0


@property
def profit_loss_percent(self):
    if self.purchase_price and self.current_price is not None:
        return (self.current_price - self.purchase_price) / self.purchase_price * 100
    return 0
