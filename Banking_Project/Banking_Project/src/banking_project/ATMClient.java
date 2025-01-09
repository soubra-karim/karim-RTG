package banking_project;

import java.awt.Font;
import javax.swing.*;
import java.awt.event.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

public class ATMClient extends JFrame implements ActionListener {

    private JTextField amountField;
    private JButton depositButton, withdrawButton, balanceButton;
    private static float balance; 
    private JLabel welcomeLabel;
    private atm atmInstance; 

    public ATMClient(atm atmInstance, String username) {
         this.atmInstance = atmInstance; 
         
        setTitle("ATM Transactions");
        setSize(500, 300);
        setLayout(null);

        welcomeLabel = new JLabel("Welcome, " + username);
        welcomeLabel.setBounds(10, 10, 300, 25);
        welcomeLabel.setFont(new Font("Serif", Font.BOLD, 20));
        add(welcomeLabel);
        
        addAmountField();
        addDepositButton();
        addWithdrawButton();
        addBalanceButton();

        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setVisible(true);
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

    private void addAmountField() {
        JLabel amountLabel = new JLabel("Amount:");
        amountLabel.setBounds(20, 50, 80, 25);
        add(amountLabel);

        amountField = new JTextField(20);
        amountField.setBounds(110, 50, 200, 25);
        add(amountField);
    }

    private void addDepositButton() {
        depositButton = new JButton("Deposit");
        depositButton.setBounds(20, 90, 150, 25); 
        depositButton.addActionListener(this);
        add(depositButton);
    }

    private void addWithdrawButton() {
        withdrawButton = new JButton("Withdraw");
        withdrawButton.setBounds(180, 90, 150, 25); 
        withdrawButton.addActionListener(this);
        add(withdrawButton);
    }

    private void addBalanceButton() {
        balanceButton = new JButton("Check Balance");
        balanceButton.setBounds(340, 90, 150, 25);
        balanceButton.addActionListener(this);
        add(balanceButton);
    }


@Override
public void actionPerformed(ActionEvent e) {
    try {
        String amountStr = amountField.getText();
        if (!"Check Balance".equals(e.getActionCommand())) {
            float amount = Float.parseFloat(amountStr);

            if (e.getSource() == depositButton) {
                String newBalance = atmInstance.deposit(amountStr); 
                JOptionPane.showMessageDialog(this, "Deposit Successful. New Balance: $" + newBalance);
            } else if (e.getSource() == withdrawButton) {
                String newBalance = atmInstance.withdraw(amountStr); 
                if (newBalance.equals("Error")) {
                    JOptionPane.showMessageDialog(this, "Insufficient funds.");
                } else {
                    JOptionPane.showMessageDialog(this, "Withdrawal Successful. New Balance: $" + newBalance);
                }
            }
        } else if (e.getSource() == balanceButton) {
            String balance = atmInstance.checkBalance(); 
            JOptionPane.showMessageDialog(this, "Current Balance: $" + balance);
        }
        amountField.setText(""); 
    } catch (NumberFormatException ex) {
        JOptionPane.showMessageDialog(this, "Please enter a valid amount.");
    } catch (Exception ex) {
        JOptionPane.showMessageDialog(this, "Operation failed: " + ex.getMessage());
    }
}


public static void main(String[] args) {
    try {
        atm atmInstance = new atm();
        atmInstance.connect(); 
        String username = null;
        SwingUtilities.invokeLater(() -> new ATMClient(atmInstance, username));
    } catch (Exception e) {
        e.printStackTrace();
    }
}
}
