GPU_MODELS = ["3090", "3080 Ti", "3080", "3070 Ti", "3070", "3060 Ti", "3060", "3050 Ti", "3050"]
GPU_SIZES = ["26GB", "24GB", "22GB", "20GB", "18GB", "16GB", "14GB", "12GB", "10GB", "8GB", "6GB", "4GB", "2GB"]

class GPU:
    def __init__(this, title = "unknow", model="unknow", price = 0, stock = 0, memerySize = "unknow"):
        this.title = title
        this.model = model
        this.price = price
        this.stock = stock
        this.memerySize = memerySize
        if (this.title != "unknow"):
            this.model = this.find_model()
            this.memerySize = this.find_memerySize()


    def set_title(this, title): this.title = title
    def set_model(this, model): this.model = model
    def set_price(this, price): this.price = price
    def set_stock(this, stock): this.stock = stock
    def set_memerySize(this, memerySize): this.memerySize = memerySize

    def get_title(this): return this.title
    def get_model(this): return this.model
    def get_price(this): return this.price
    def get_stock(this): return this.stock
    def get_memerySize(this): return this.memerySize

    def find_model(this):
        for model in GPU_MODELS:
            if (this.title.find(model) != -1):
                return model
        return "unknow"

    def find_memerySize(this):
        for size in GPU_SIZES:
            if (this.title.find(size) != -1):
                return size
        return "unknow"
    
    def string(this):
        return this.model + " " + this.memerySize + " " + str(this.price) + " " + str(this.stock)
