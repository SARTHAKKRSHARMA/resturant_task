All the views in the this projects are listed here:

"register/" To register user(both staff and customer),if registered as staff then you'll be able to login once your account is activated by admin

"login/" For logging user

"/" Depending on wether user is logged in or not

"logout/" to log user out

"<str:food_category>/" If a food category is selected then food item under that category are visible

"item/<slug:food_item>/" To get a detail view of a item, and from here only you can add item to cart

"cart/" To view cart

"cart/<slug:coupon>/" To apply coupon

"empty/cart" To  empty cart

"addresses/" To get the list of addresses of logged in user

"previous/order" To get the list of previous order

"feedback/<int:id> To provide feedback for the order, you can provide feedback only once an order is delivered

"create_coupons/" only staff members can access this view, to create coupon, and once a coupon is created succesfully mail is sent to respective users about the coupon

"premium/" To change the subscription of customer

"view/meal" To view various meals

"add/meal/<int:id>" To  add the meal into the cart

"create/meal" Can only be accessed by staff member to create meal

"meal/<int:id>" To add a item into the meal

"item/remove/<int:id> To remove item from the meal

'filter/price" To filter the items on the basis of price

"search/item" implementation of search bar

"available/items/" To filter the items which are available right now
