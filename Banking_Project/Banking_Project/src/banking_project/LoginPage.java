package banking_project;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.io.FileNotFoundException;

public class LoginPage extends JFrame implements ActionListener {

    private JTextField userTextField;
    private JPasswordField passwordField;
    private JButton loginButton;
    private atm atmInstance;

    public LoginPage(atm atmInstance) {
        this.atmInstance = atmInstance;
        
        setTitle("ATM Login");
        setSize(400, 200);
        setLayout(null);

        addUsernameField();
        addPasswordField();
        addLoginButton();

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
        setLocationRelativeTo(null);
    }

    private void addUsernameField() {
        JLabel userLabel = new JLabel("Username:");
        userLabel.setBounds(20, 20, 80, 25);
        add(userLabel);

        userTextField = new JTextField(20);
        userTextField.setBounds(100, 20, 165, 25);
        add(userTextField);
    }

    private void addPasswordField() {
        JLabel passwordLabel = new JLabel("Password:");
        passwordLabel.setBounds(20, 50, 80, 25);
        add(passwordLabel);

        passwordField = new JPasswordField(20);
        passwordField.setBounds(100, 50, 165, 25);
        add(passwordField);
    }

    private void addLoginButton() {
        loginButton = new JButton("Login");
        loginButton.setBounds(100, 80, 80, 25);
        loginButton.addActionListener(this);
        add(loginButton);
    }

    @Override
        public void actionPerformed(ActionEvent e) {
            String username = userTextField.getText();
            String password = new String(passwordField.getPassword());

            try {
                boolean isLoggedIn = atmInstance.login(username, password);
                if (isLoggedIn) {
                    JOptionPane.showMessageDialog(this, "Login Successful");
                    this.setVisible(false);
                    new ATMClient(atmInstance, username);
                } else {
                    JOptionPane.showMessageDialog(this, "Invalid username or password.");
                }
            } catch (Exception exception) {
                exception.printStackTrace();
                JOptionPane.showMessageDialog(this, "Error during login: " + exception.getMessage());
            }
        }
    public static void main(String[] args) {
        try {
            atm atmInstance = new atm(); 
            atmInstance.connect(); 
            SwingUtilities.invokeLater(() -> new LoginPage(atmInstance));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
