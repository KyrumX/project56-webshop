from ..models import Products, ProductDetails

def editProduct(request, item):
    updateProduct = Products.objects.get(prodNum=item)
    updateProductDetails = ProductDetails.objects.get(prodNum=Products(item))
    updateProduct.prodName = request.POST.get('prodName', '')
    updateProduct.prodStock = request.POST.get('prodStock', '')
    updateProductDetails.genre = request.POST.get('genre', '')
    updateProductDetails.type = request.POST.get('type', '')
    updateProductDetails.publisher = request.POST.get('publisher', '')
    updateProductDetails.totalPages = request.POST.get('totalPages', '')
    updateProductDetails.language = request.POST.get('language', '')
    updateProductDetails.rating = request.POST.get('rating', '')
    updateProductDetails.author = request.POST.get('author', '')
    updateProductDetails.desc = request.POST.get('desc', '')
    updateProductDetails.imageLink = request.POST.get('imageLink', '')
    updateProductDetails.pubDatum = request.POST.get('pubDatum', '')
    updateProduct.save()
    updateProductDetails.save()

def checkIfProductExist(item):
    return Products.objects.filter(prodNum=item).exists()

def deleteProduct(request):
    item = int(request.POST['deleteproduct'])
    if checkIfProductExist(item):
        Products.objects.filter(prodNum=item).delete()

