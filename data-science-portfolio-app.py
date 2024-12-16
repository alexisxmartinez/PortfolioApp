import streamlit as st
import json
from pathlib import Path

class PortfolioApp:
    def __init__(self, projects_file='projects.json'):
        """
        Initialize the portfolio application
        
        Args:
            projects_file (str): Path to the JSON file containing project details
        """
        self.projects_file = projects_file
        self.projects = self.load_projects()
        
    def load_projects(self):
        """
        Load projects from a JSON file
        
        Returns:
            dict: Dictionary of projects organized by categories
        """
        try:
            with open(self.projects_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error(f"Projects file '{self.projects_file}' not found!")
            return {}
        
    def display_project_grid(self, category=None):
        """
        Display projects in a grid layout
        
        Args:
            category (str, optional): Specific category to filter projects
        """
        # Determine which projects to show
        display_projects = self.projects
        if category:
            display_projects = {category: self.projects.get(category, {})}
        
        # Create columns for category navigation
        categories = list(self.projects.keys())
        col_width = max(3, 12 // len(categories)) if categories else 12
        nav_cols = st.columns(len(categories) or 1)
        
        # Category navigation
        selected_category = None
        for i, cat in enumerate(categories):
            with nav_cols[i]:
                if st.button(cat, use_container_width=True):
                    selected_category = cat
        
        # Project display
        for cat, projects in display_projects.items():
            if category and cat != category:
                continue
            
            st.subheader(cat)
            
            # Create rows of projects
            project_cols = st.columns(3)
            col_index = 0
            
            for project_name, project_details in projects.items():
                with project_cols[col_index]:
                    # Display project image with hover description
                    st.image(project_details['image'], 
                             caption=project_name, 
                             use_column_width=True)
                    
                    # Expander for project details
                    with st.expander("Project Details"):
                        st.write(project_details['description'])
                        st.write(f"**Technologies:** {project_details.get('technologies', 'N/A')}")
                        
                        # Optional GitHub/Demo links
                        if 'github_link' in project_details:
                            st.markdown(f"[GitHub Repository]({project_details['github_link']})")
                        if 'demo_link' in project_details:
                            st.markdown(f"[Live Demo]({project_details['demo_link']})")
                
                # Move to next column, reset if needed
                col_index = (col_index + 1) % 3
    
    def run(self):
        """
        Run the Streamlit application
        """
        st.set_page_config(page_title="Data Science Portfolio", 
                            page_icon=":rocket:", 
                            layout="wide")
        
        # Title and introduction
        st.title("Data Science Portfolio")
        st.write("Showcasing my data science and machine learning projects")
        
        # Display all projects
        self.display_project_grid()

def main():
    portfolio = PortfolioApp()
    portfolio.run()

if __name__ == "__main__":
    main()
