	package view;

import java.awt.BorderLayout;
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.SwingConstants;
import javax.swing.JLabel;

public class TelaContador extends JFrame {

	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private Integer contador;
	private JLabel nCliqueLabel;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					TelaContador frame = new TelaContador();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public TelaContador() {
		contador = 0;
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 450, 300);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		
		JButton clicarButton = new JButton("Clique");
		clicarButton.setVerticalAlignment(SwingConstants.TOP);
		
		clicarButton.addActionListener(e -> incrementarContador());
		
		contentPane.add(clicarButton);
		
		nCliqueLabel = new JLabel("Cliques: 0");
		contentPane.add(nCliqueLabel);

	}
	
	private void incrementarContador() {
		contador++;
		nCliqueLabel.setText("Cliques: " + contador);
		System.out.println(contador);
	}

}