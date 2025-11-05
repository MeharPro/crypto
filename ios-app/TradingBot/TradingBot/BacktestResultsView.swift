import SwiftUI

struct BacktestResultsView: View {
    let results: [String: Any]

    var body: some View {
        Form {
            Section(header: Text("Summary")) {
                ResultRow(label: "Initial Capital", value: results["initial_capital"] as? Double ?? 0)
                ResultRow(label: "Final Portfolio Value", value: results["final_portfolio_value"] as? Double ?? 0)
                ResultRow(label: "Profit/Loss", value: results["profit_loss"] as? Double ?? 0)
            }

            Section(header: Text("Trades")) {
                if let trades = results["trades"] as? [String], !trades.isEmpty {
                    List(trades, id: \.self) { trade in
                        Text(trade)
                    }
                } else {
                    Text("No trades were executed.")
                }
            }
        }
        .navigationTitle("Backtest Results")
    }
}

struct ResultRow: View {
    let label: String
    let value: Double

    var body: some View {
        HStack {
            Text(label)
            Spacer()
            Text(String(format: "$%.2f", value))
        }
    }
}

struct BacktestResultsView_Previews: PreviewProvider {
    static var previews: some View {
        BacktestResultsView(results: [
            "initial_capital": 10000.0,
            "final_portfolio_value": 12500.0,
            "profit_loss": 2500.0,
            "trades": ["BOUGHT 10.00 of AAPL at $150.00", "SOLD 10.00 of AAPL at $175.00"]
        ])
    }
}
