from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AccountLoginSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['account:login']
    
    def location(self, item):
        return reverse('account:login')  # Ana sayfa URL'si
      
class AccountRegisterSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['account:register']
    
    def location(self, item):
        return reverse('account:register')  # Ana sayfa URL'si
