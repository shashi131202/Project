import java.sql.*;

public class SupermarketManager {
    // Database connection parameters
    private static final String DB_URL = "jdbc:mysql://localhost:3306/super";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "yash0409";

    public void displayAvailableProducts() {
        try {
            Connection connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
            Statement statement = connection.createStatement();
            String query = "SELECT * FROM products";
            ResultSet resultSet = statement.executeQuery(query);

            System.out.println("These are available in our supermarket:");
            while (resultSet.next()) {
                int productID = resultSet.getInt("Product_ID");
                String productName = resultSet.getString("Name_of_product");
                System.out.println("ID: " + productID + " | NAME: " + productName);
            }

            resultSet.close();
            statement.close();
            connection.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        SupermarketManager manager = new SupermarketManager();
        manager.displayAvailableProducts();
    }
}
