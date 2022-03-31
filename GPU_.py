GPU_MODELS = ["3090 Ti", "3090", "3080 Ti", "3080", "3070 Ti", "3070", "3060 Ti", "3060", "3050 Ti", "3050"]
GPU_SIZES = ["26GB", "24GB", "22GB", "20GB", "18GB", "16GB", "14GB", "12GB", "10GB", "8GB", "6GB", "4GB", "2GB"]
GPU_BRANDS = ["ASUS", "Gigabyte", "MSI", "EVGA", "Zotac", "PowerColor", "PNY", "Sapphire Technology", "Visiontek", "ASRock", "AMD"]

class GPU:
    def __init__(this, title = "unknow", model="unknow", brand = "unknow", price = 0, stock = 0, memorySize = "unknow", SKU = "unknow", link = "unknow"):
        this.title = title
        this.model = model
        this.brand = brand
        this.price = price
        this.stock = stock
        this.memorySize = memorySize
        this.SKU = SKU
        this.link = link
        if (this.title != "unknow"):
            this.model = this.find_model()
            this.brand = this.find_brand()
            this.memorySize = this.find_memorySize()

    def set_title(this, title): this.title = title
    def set_model(this, model): this.model = model
    def set_brand(this, brand): this.brand = brand
    def set_price(this, price): this.price = price
    def set_stock(this, stock): this.stock = stock
    def set_memorySize(this, memorySize): this.memorySize = memorySize
    def set_SKU(this, SKU): this.SKU = SKU
    def set_link(this, link): this.link = link

    def get_title(this): return this.title
    def get_model(this): return this.model
    def get_brand(this): return this.brand
    def get_price(this): return this.price
    def get_stock(this): return this.stock
    def get_memorySize(this): return this.memorySize
    def get_SKU(this): return this.SKU
    def get_link(this): return this.link

    def find_model(this):
        for model in GPU_MODELS:
            if (this.title.find('3090TI') != -1):
                return '3090 Ti'
            if (this.title.find(model) != -1):
                return model
        return "unknow"

    def find_memorySize(this):
        for size in GPU_SIZES:
            if (this.title.find(size) != -1):
                return size
        return "unknow"
    
    def find_brand(this):
        for brand in GPU_BRANDS:
            if (this.title.find(brand) != -1):
                return brand
        return "unknow"
    
    def string(this):
        return this.model + " " + this.memorySize + " " + str(this.price) + " " + str(this.stock)
