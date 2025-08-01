import java.sql.*;
import java.util.*;
class SuperMarket{
public void trackPurchases(int id, List<ProductPurchase> purchasedProducts) {
try {
Connection c = DriverManager.getConnection("jdbc:mysql://localhost:3306/super", "root", "password");
String q = "INSERT INTO purchases (id, product_name, quantity, total_cost) VALUES (?, ?, ?, ?)";
PreparedStatement ps = c.prepareStatement(q);
for (ProductPurchase purchase : purchasedProducts) {
ps.setInt(1, id);
ps.setString(2, purchase.name);
ps.setInt(3, purchase.quantity);
ps.setDouble(4, purchase.item);
ps.executeUpdate();
}
ps.close();
c.close();
} catch (Exception e) {
e.printStackTrace();
}
}
public void Customer(){
Scanner sc=new Scanner(System.in);
String user=sc.next();
String pass=sc.next();
try{
System.out.println("Enter customer id");
int id=sc.nextInt();
if(id==0){
System.out.println("no products purchased");
}
else{
System.out.println("Enter customer name");
String name=sc.next();
System.out.println("Enter customer phone no");
int phone=sc.nextInt();
System.out.println("Enter customer bill");
double bill=sc.nextDouble();
Connection co=DriverManager.getConnection("jdbc:mysql://localhost:3306/super",user,pass);
String q="insert into customer(name,phone_no,bill) values(?,?,?)";
PreparedStatement ps=co.prepareStatement(q);
ps.setString(1,name);
ps.setInt(2,phone);
ps.setDouble(3,bill);
ps.execute();
co.close();
}
}
catch(Exception e){
e.printStackTrace();
}
}
public void list(){
try{
Scanner sc=new Scanner(System.in);
System.out.print("These are available in our supermarket\n");
Connection c=DriverManager.getConnection("jdbc:mysql://localhost:3306/super","root","yash0409");
Statement st=c.createStatement();
String ab="select * from products";
ResultSet r=st.executeQuery(ab);
while(r.next()){
System.out.print("ID: "+r.getInt("Product_ID")+" ");
System.out.print("|NAME: "+r.getString("Name_of_product")+"\n");
}

while(true){
System.out.print("Enter the id of the product to check its price and quantity available(press 0 to exit): ");
int a;
while(true){ 
try{
a=sc.nextInt();
break;
}
catch(InputMismatchException e){
System.out.println("enter correct number");
sc.next();
}
}
if(a<6 && a>0){
String d="select Name_of_product,Qunatity_Available,Price_Of_Product from products where  Product_ID=?";
PreparedStatement ps=c.prepareStatement(d);
ps.setInt(1,a);
ResultSet rs=ps.executeQuery();
while(rs.next()){
System.out.print("NAME: "+rs.getString("Name_of_product")+" ");
System.out.print("|Quantity Availabe: "+rs.getInt("Qunatity_Available")+" ");
System.out.print("|Cost: "+rs.getFloat("Price_Of_Product")+"\n");
break;
}

}
else if(a==0){
break;
}
else{
System.out.println("enter correct id:");
continue;
}
}
}
catch(Exception e){
e.printStackTrace();
}
}

class ProductPurchase{
String name;
float cost;
int quantity;
double item;
public ProductPurchase(String name,float cost,int quantity,double item){
this.name=name;
this.cost=cost;
this.quantity=quantity;
this.item=item;
}
}
public void Bill(){
try{
Scanner sc=new Scanner(System.in);
double bill=0.0;
List<ProductPurchase> purchasedProducts = new ArrayList<>();
Connection c=DriverManager.getConnection("jdbc:mysql://localhost:3306/super","root","yash0409");
String d="select Name_of_product,Price_Of_Product,Qunatity_Available from products where Product_ID=?";
while(true){
System.out.println("Enter the product id to purchase the item(enter 0 to exit)");
int a;
while(true){ 
try{
a=sc.nextInt();
break;
}
catch(InputMismatchException e){
System.out.println("enter correct number");
sc.next();
}
}

if(a==0){
System.out.println("thank u for shopping");
break;
}
else{
PreparedStatement ps=c.prepareStatement(d);
ps.setInt(1,a);
ResultSet rs=ps.executeQuery();
if(rs.next()){
String name=rs.getString("Name_of_product");
Float cost=rs.getFloat("Price_Of_Product");
int availableQuantity = rs.getInt("Qunatity_Available");
System.out.print("name: "+name);
System.out.print(" cost: "+cost+"\n");
if(availableQuantity<=0){
System.out.println("Product not available at present");
continue;
}
System.out.println("Enter the Quantity:");
int quantity=sc.nextInt();
if(availableQuantity<quantity){
System.out.println("Quantity not avaialable please enter correct number");
continue;
}
double item=cost*quantity;
System.out.println("cost of the item is:"+item);
bill+=item;
ProductPurchase purchase = new ProductPurchase(name, cost, quantity, item);                        purchasedProducts.add(purchase);
int remainingQuantity = availableQuantity - quantity;
String updateQuery = "UPDATE products SET Qunatity_Available=? WHERE Product_ID=?";
PreparedStatement up = c.prepareStatement(updateQuery);
up.setInt(1, remainingQuantity);
up.setInt(2, a);
up.executeUpdate();

}
else{
System.out.println("product not found");
}
}
}
System.out.println("Products Purchased:");
for (ProductPurchase purchase : purchasedProducts) {
System.out.println(purchase.name + " | Quantity: " + purchase.quantity + " | Cost: " + purchase.item);
}
double gst=bill*0.2;
double discount=bill*0.3;
double total=bill+gst-discount;
System.out.println("the bill without discount is: "+bill);
System.out.println("the total bill with discount is :"+total);
System.out.println("enter the id of customer");
int id = sc.nextInt();
trackPurchases(id, purchasedProducts);
}
catch(Exception e){
e.printStackTrace();
}
}
public static void main(String args[]){
SuperMarket s=new SuperMarket();
s.list();
s.Bill();
s.Customer();
}
}
