package banking_project;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.IOException; 

public class SignUpPage extends JFrame implements ActionListener {

    private JLabel userLabel, passwordLabel;
    private JTextField userTextField;
    private JPasswordField passwordField;
    private JButton registerButton;
    private atm atmInstance;

    public SignUpPage(atm atmInstance) {
        this.atmInstance = atmInstance;
        
        setTitle("Signup Page");

        int frameWidth = 400;
        int frameHeight = 200;
        setSize(frameWidth, frameHeight);

        // Username Label
        userLabel = new JLabel("Username:");
        userLabel.setBounds(20, 20, 100, 30); 
        add(userLabel);

        // Username Field
        userTextField = new JTextField();
        userTextField.setBounds(130, 20, 230, 30); 
        add(userTextField);

        // Password Label
        passwordLabel = new JLabel("Password:");
        passwordLabel.setBounds(20, 60, 100, 30); 
        add(passwordLabel);

        // Password Field
        passwordField = new JPasswordField();
        passwordField.setBounds(130, 60, 230, 30);
        add(passwordField);

        // Register Button
        registerButton = new JButton("Register");
        registerButton.setBounds(130, 100, 230, 30); 
        registerButton.addActionListener(this);
        add(registerButton);

        // Frame settings
        setLayout(null);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Center the frame on the screen
        setLocationRelativeTo(null);
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                try {
                    atmInstance.closeConnection(); 
                    System.out.println("Connection closed.");
                } catch (IOException ioException) {
                    ioException.printStackTrace(); 
                }
            }
        });
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == registerButton) {
            String username = userTextField.getText();
            String password = new String(passwordField.getPassword());

            try {
                boolean isRegistered = atmInstance.register(username, password);
                if (isRegistered) {
                    JOptionPane.showMessageDialog(this, "Registration Successful for: " + username);
                } else {
                    JOptionPane.showMessageDialog(this, "Registration Failed. User already exists.");
                }
            } catch (Exception exception) { 
                exception.printStackTrace();
                JOptionPane.showMessageDialog(this, "Error during registration: " + exception.getMessage());
            }

            userTextField.setText("");
            passwordField.setText("");
        }
    }

    public static void main(String[] args) {
       try {
            atm atmInstance = new atm();
            atmInstance.connect();
            SwingUtilities.invokeLater(() -> new SignUpPage(atmInstance));
        } catch (Exception e) {
            e.printStackTrace();
        } 
    }
}
