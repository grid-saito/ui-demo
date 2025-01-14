import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from utils import save_session_settings, get_session_settings
import plotly.graph_objects as go
from services.graph import chat_about_demand_data, get_suggested_actions


def demand_forecast_dialog(demand_forecast_before: dict, demand_forecast_after: dict):
    """
    Render demand curves with before/after comparison and expert recommendations.
    
    Parameters:
        demand_forecast_before (dict): Previous demand forecast with dates and values
        demand_forecast_after (dict): New demand forecast with dates and values
    """
    @st.dialog("Demand Forecast", width="large")
    def show_dialogue():
        # Create two columns - left for graphs, right for recommendations
        col1, col2 = st.columns([0.6, 0.4])
        
        with col1:
            # Filter data to only show future forecasts
            current_time = datetime.now()
            demand_forecast_before["Timestamp"] = pd.to_datetime(demand_forecast_before["Timestamp"])
            demand_forecast_after["Timestamp"] = pd.to_datetime(demand_forecast_after["Timestamp"])
            future_timestamps = [t for t in demand_forecast_before["Timestamp"] if t > current_time]
            future_demand_before = {
                "Timestamp": future_timestamps,
                "Demand": [d for t, d in zip(demand_forecast_before["Timestamp"], demand_forecast_before["Demand"]) if t > current_time]
            }
            future_demand_after = {
                "Timestamp": future_timestamps,
                "Demand": [d for t, d in zip(demand_forecast_after["Timestamp"], demand_forecast_after["Demand"]) if t > current_time]
            }

            # Before plot with future data only
            fig1 = go.Figure()

            # Generate estimates for before forecast
            before_estimates = {
                "High Estimate": [v + 150 for v in future_demand_before["Demand"]],
                "Average Estimate": future_demand_before["Demand"],
                "Low Estimate": [v - 150 for v in future_demand_before["Demand"]]
            }
        
            colors = {"High Estimate": "orange", "Average Estimate": "green", "Low Estimate": "red"}
            dash_styles = {"High Estimate": "dash", "Average Estimate": "dashdot", "Low Estimate": "dash"}

            for estimate_type, values in before_estimates.items():
                fig1.add_trace(go.Scatter(
                    x=future_demand_before["Timestamp"],
                    y=values,
                    name=estimate_type,
                    line=dict(
                        color=colors[estimate_type],
                        dash=dash_styles[estimate_type]
                    )
                ))
        
            fig1.update_layout(
                height=250,
                margin=dict(l=50, r=50, t=30, b=30),
                title="Current Demand Forecast",
                showlegend=True
            )
            st.plotly_chart(fig1, use_container_width=True)
        
            # Down arrow
            st.markdown(
                """
                <div style='text-align: center; margin: 10px 0;'>
                    <span style='font-size: 24px; color: #666;'>⬇️</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        
            # After plot with future data only
            fig2 = go.Figure()
        
            # Generate estimates for after forecast
            after_estimates = {
                "High Estimate": [v + 150 for v in future_demand_after["Demand"]],
                "Average Estimate": future_demand_after["Demand"],
                "Low Estimate": [v - 150 for v in future_demand_after["Demand"]]
            }
        
            for estimate_type, values in after_estimates.items():
                fig2.add_trace(go.Scatter(
                    x=future_demand_after["Timestamp"],
                    y=values,
                    name=estimate_type,
                    line=dict(
                        color=colors[estimate_type],
                        dash=dash_styles[estimate_type]
                    )
                ))
        
            fig2.update_layout(
                height=250,
                margin=dict(l=50, r=50, t=30, b=30),
                title="New Demand Forecast",
                showlegend=True
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            avg_before = sum(demand_forecast_before["Demand"]) / len(demand_forecast_before["Demand"])
            avg_after = sum(demand_forecast_after["Demand"]) / len(demand_forecast_after["Demand"])
            percent_change = ((avg_after - avg_before) / avg_before) * 100

            # Expert Opinion 1 - Conservative View
            st.markdown(
                f"""
                <div style='padding: 15px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;'>
                    <div style='display: flex; align-items: center;'>
                        <span style='color: #d9534f; font-size: 24px; margin-right: 10px;'>❌</span>
                        <div>
                            <strong>Power Systems Expert 1</strong><br>
                            "The forecast seems too optimistic. Given recent economic indicators 
                            and historical patterns, I expect demand to be lower. We should 
                            consider a more conservative estimate for planning purposes."
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Expert Opinion 2 - Optimistic View
            st.markdown(
                f"""
                <div style='padding: 15px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;'>
                    <div style='display: flex; align-items: center;'>
                        <span style='color: #5cb85c; font-size: 24px; margin-right: 10px;'>✅</span>
                        <div>
                            <strong>Power Systems Expert 2</strong><br>
                            "The forecast aligns with our growth projections. Recent industrial 
                            development in the region suggests we might even see higher demand 
                            peaks than predicted."
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Expert Opinion 3 - Balanced View
            st.markdown(
                f"""
                <div style='padding: 15px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;'>
                    <div style='display: flex; align-items: center;'>
                        <span style='color: #5cb85c; font-size: 24px; margin-right: 10px;'>✅</span>
                        <div>
                            <strong>Power Systems Expert 3</strong><br>
                            "The {percent_change:.1f}% {'increase' if percent_change > 0 else 'decrease'} 
                            aligns with our market analysis. The forecast accounts for seasonal 
                            variations and growth trends appropriately."
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Expert Summary with distinct style
            st.markdown(
                f"""
                <div style='
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 5px;
                    background: white;
                    border: 1px solid #ddd;
                '>
                    <div style='
                        border-bottom: 2px solid #333;
                        margin-bottom: 10px;
                        padding-bottom: 5px;
                    '>
                        <strong style='
                            color: #333;
                            font-size: 1.1em;
                        '>Expert Summary</strong>
                    </div>
                    <div style='color: #333;'>
                        Based on the expert analysis, the updated demand forecast provides a balanced 
                        view of future demand. While there are differing opinions on the trend, 
                        the forecast serves as a reasonable baseline for planning purposes.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        button_container = st.container()
        with button_container:
            # Use columns to push buttons to the right
            _, _, col_btn1, col_btn2 = st.columns([0.4, 0.4, 0.1, 0.1])
            with col_btn1:
                if st.button("Confirm Changes", type="primary"):
                    st.session_state["demand_forecast"] = demand_forecast_after
                    st.session_state["demand_forecast_dialogue_closed"] = True
                    st.rerun()
            with col_btn2:
                if st.button("Revert Changes", type="secondary"):
                    st.session_state["demand_forecast"] = demand_forecast_before
                    st.rerun() 
        st.html("<span class='big-dialog'></span>") 
    show_dialogue()


def render_demand_curves(demand_data, results_data):
    """
    Render demand curves with observed data, forecasted data, and results.
    Results are plotted as a distinct curve for easy identification, aligned to the same time range as demand data.

    Args:
        demand_data (pd.DataFrame): DataFrame containing demand data with columns Timestamp and Demand.
        results_data (pd.DataFrame): DataFrame containing results data with columns Timestamp and Result.
    """
    demand_data["Timestamp"] = pd.to_datetime(demand_data["Timestamp"])

    # Separate past and future data
    today = datetime.now()
    past_data = demand_data[demand_data["Timestamp"] <= today]
    future_data = demand_data[demand_data["Timestamp"] > today]

    # Append the last observed value to the start of the forecast
    if not past_data.empty and not future_data.empty:
        future_data = future_data.copy()
        future_data.iloc[0, 1] = past_data.iloc[-1, 1]  # Ensure continuity

    # Create the figure
    fig, ax = plt.subplots(figsize=(12, 4))  # Larger figure for better readability

    # Plot past data with a solid line
    #ax.plot(
    #    past_data["Timestamp"],
    #    past_data["Demand"],
    #    label="Observed",
    #    linestyle="-",
    #    color="blue",
    #    linewidth=2,
    #)

    # Generate high, average, and low forecasts
    forecasts = {
        "High Estimate": future_data["Demand"] + 150,  # High demand offset
        "Average Estimate": future_data["Demand"],  # No offset
        "Low Estimate": future_data["Demand"] - 150,  # Low demand offset
    }

    colors = {"High Estimate": "orange", "Average Estimate": "green", "Low Estimate": "red"}
    linestyles = {"High Estimate": "--", "Average Estimate": "-.", "Low Estimate": "--"}

    # Plot forecasts with appropriate styles
    for label, forecast_data in forecasts.items():
        forecast_data.iloc[0] = past_data.iloc[-1]["Demand"]  # Ensure continuity
        ax.plot(
            future_data["Timestamp"],
            forecast_data,
            label=label,
            linestyle=linestyles[label],
            linewidth=1.5,
            color=colors[label],
            alpha=0.8,
        )

    # Add results as a separate curve
    if (results_data is not None):
        results_df = pd.DataFrame(results_data)
        results_df["Timestamp"] = results_data["Timestamp"]
        results_df["Total_Output"] = results_df.drop(columns=["Timestamp"]).sum(axis=1)
        results_df["Total_Output"].iloc[0] = 0
        results_df["Total_Output"].iloc[1] = 0
        # Create the bar plot
        ax.bar(
            results_df["Timestamp"],
            results_df["Total_Output"],
            label="Total Results Output",
            color="purple",
            alpha=0.7,  # Optional transparency
        )
        st.session_state["external_data"]["Total_Output"] = results_df["Total_Output"]

    # Add labels, title, and legend
    ax.set_title("Demand Trend", fontsize=16, fontweight="bold")
    ax.set_xlabel("Timestamp", fontsize=12)
    ax.set_ylabel("Demand (GW)", fontsize=12)
    ax.set_ylim(0, 2200)  # Set fixed y-axis limits
    ax.tick_params(axis="x", labelrotation=45, labelsize=10)
    ax.tick_params(axis="y", labelsize=10)
    ax.legend(
        fontsize=10,
        loc="upper left",
        bbox_to_anchor=(1, 1),  # Place legend outside graph
        borderaxespad=0,  # No padding between axes and legend
    )
    plt.tight_layout()

    # Display the figure in Streamlit
    st.pyplot(fig)


def render_demand_curves_in_dialogue(demand_data, demand_constraint):
    """
    Render demand curves with observed data, forecasted data, and demand constraints.
    """
    # Create DataFrame for demand constraints
    demand_constraint_df = pd.DataFrame({
        "Timestamp": demand_data["Timestamp"],
        "Constraint": demand_constraint
    })

    demand_constraint_df["Timestamp"] = pd.to_datetime(demand_constraint_df["Timestamp"])
    demand_data["Timestamp"] = pd.to_datetime(demand_data["Timestamp"])
    # Separate past and future data
    today = datetime.now()
    past_data = demand_data[demand_data["Timestamp"] <= today]
    future_data = demand_data[demand_data["Timestamp"] > today]
    future_constraint = demand_constraint_df[demand_constraint_df["Timestamp"] > today]

    if not past_data.empty and not future_data.empty:
        future_data = future_data.copy()
        future_data.iloc[0, 1] = past_data.iloc[-1, 1]  # Ensure continuity

    # Create the figure
    fig, ax = plt.subplots(figsize=(12, 4))

    # Generate high, average, and low forecasts
    forecasts = {
        "High Estimate": future_data["Demand"] + 150,
        "Average Estimate": future_data["Demand"],
        "Low Estimate": future_data["Demand"] - 150,
    }

    colors = {"High Estimate": "orange", "Average Estimate": "green", "Low Estimate": "red"}
    linestyles = {"High Estimate": "--", "Average Estimate": "-.", "Low Estimate": "--"}

    # Plot forecasts with appropriate styles
    for label, forecast_data in forecasts.items():
        forecast_data.iloc[0] = past_data.iloc[-1]["Demand"]  # Ensure continuity
        ax.plot(
            future_data["Timestamp"],
            forecast_data,
            label=label,
            linestyle=linestyles[label],
            linewidth=1.5,
            color=colors[label],
            alpha=0.8,
        )

    # Add demand constraints as bars
    if not future_constraint.empty:
        ax.bar(
            future_constraint["Timestamp"],
            future_constraint["Constraint"],
            label="Demand Constraints",
            color="grey",
            alpha=0.3,
        )

    # Add labels, title, and legend
    ax.set_title("Demand Forecast & Constraints", fontsize=16, fontweight="bold")
    ax.set_xlabel("Timestamp", fontsize=12)
    ax.set_ylabel("Demand (GW)", fontsize=12)
    ax.set_ylim(0, 2200)  # Set fixed y-axis limits
    ax.tick_params(axis="x", labelrotation=45, labelsize=10)
    ax.tick_params(axis="y", labelsize=10)
    ax.legend(
        fontsize=10,
        loc="upper left",
        bbox_to_anchor=(1, 1),
        borderaxespad=0,
    )
    plt.tight_layout()

    # Display the figure in Streamlit
    st.pyplot(fig)


def demand_constraint_settings_panel(settings, id="demand_constraint_settings_panel"):
    """
    Display and edit demand constraints in a transposed table format.
    Rows represent different demand values, columns represent timesteps.
    """
    # Create DataFrame with single row of demand values
    demand_df = pd.DataFrame(
        {
            f"Timestep {i+1}": [value] for i, value in enumerate(settings["demand"])
        },
        index=["Demand (GW)"]
    )
    
    # Use data editor with transposed view
    edited_demand = st.data_editor(
        demand_df,
        num_rows="fixed",
        key=f"demand_table_{id}"
    )
    
    # Extract values from the row and update settings
    settings["demand"] = edited_demand.iloc[0].tolist()
    save_session_settings(settings)



def demand_constraint_dialog():
    """
    Show a dialog with demand forecast and constraint settings.
    """
    @st.dialog("Demand Settings", width="large")
    def show_dialogue():
        # Create two columns with 7:3 ratio
        col1, col2 = st.columns([0.7, 0.3])
        
        # Left column - Graph and Settings
        with col1:
            st.subheader("Demand Forecast")
            demand_data = st.session_state.external_data["demand_data"]
            demand_constraint = get_session_settings()["demand"]
            render_demand_curves_in_dialogue(demand_data, demand_constraint)
            
            st.write("---")
            
            st.subheader("Demand Constraint Settings")
            settings = get_session_settings()
            demand_constraint_settings_panel(settings, id="demand_dialogue")
        
        # Right column - Suggestions and Chat
        with col2:
            st.write("### Suggested Actions")
            
            suggestions = [
                "Set demand constraint to high forecast",
                "Set demand constraint to low forecast",
                "Increase demand constraint by 100 units",
                "Decrease demand constraint by 100 units",
                "Set demand constraint to average forecast",
                "Set demand constraint to match peak hours",
            ]
            
            selected_suggestion = st.pills(
                "Select an action",
                suggestions,
                selection_mode="single",
                label_visibility="visible",
            )
            
            st.write("---")
            default_message = "Process demand constraint"
            user_message = st.chat_input(default_message)            
            def process_demand_constraint(user_message):
                response = chat_about_demand_data(
                    user_message, 
                    [], # Empty list since we're not storing history
                    demand_constraint, 
                    demand_data
                )
                st.markdown(
                    f"""
                    <div style='
                        padding: 15px;
                        margin: 10px 0;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        background-color: #f8f9fa;
                    '>
                        <div style='display: flex; align-items: center;'>
                            <span style='color: #0275d8; font-size: 24px; margin-right: 10px;'>💡</span>
                            <div>
                                <strong>Assistant</strong><br>
                                {response["output"]}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            if selected_suggestion:
                process_demand_constraint(selected_suggestion)
            else: 
                process_demand_constraint(user_message)
        
        st.html("<span class='big-dialog'></span>")
        if st.button("Close"):
            st.rerun()
            
    st.html("<span class='big-dialog'></span>")
    show_dialogue()