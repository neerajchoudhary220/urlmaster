from services.cloudflared import get_tunnel

public_url  = get_tunnel('http://laravel_test1.test')
print(public_url)