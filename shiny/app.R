library(shiny)
library(vroom)
library(dplyr)
library(ggplot2)
library(tidyquant)
library(scales)

data <- vroom::vroom("../data/processed/angel.csv")

ui <- fluidPage(
  titlePanel("TheGym - Angel, London"),
  sidebarLayout(
    sidebarPanel(
      sliderInput(
        "dates", "Select time period",
        min = as.Date("2021-04-25"),
        max = as.Date("2022-01-22"),
        value = c(as.Date("2021-11-01"), as.Date("2021-12-01"))
      ),
      numericInput("days_rolling", "Rolling average (n days)",
        value = 7,
        min = 1, max = 30
      )
    ),
    mainPanel(
      fluidRow(plotOutput("plot")),
      fluidRow(
        column(3, plotOutput("plot_mon")),
        column(3, plotOutput("plot_tue")),
        column(3, plotOutput("plot_wed")),
        column(3, plotOutput("plot_thu")),
      ),
      fluidRow(
        column(3, plotOutput("plot_fri")),
        column(3, plotOutput("plot_sat")),
        column(3, plotOutput("plot_sun")),
      )
    )
  )
)

server <- function(input, output, session) {
  filtered_data <- reactive({
    data %>%
      filter(as.Date(time) >= input$dates[1] &
        as.Date(time) <= input$dates[2]) %>%
      mutate(day_of_week = lubridate::wday(time, week_start = 1))
  })
  output$plot <- renderPlot(
    filtered_data() %>%
      ggplot(aes(time, capacity)) +
      geom_line() +
      geom_ma(
        ma_fun = SMA, n = 4 * 24 * input$days_rolling,
        col = "red", linetype = "solid"
      )
  )
  plot_day <- function(day, day_id) {
    renderPlot(
      filtered_data() %>% filter(day_of_week == day_id) %>%
        mutate(time = format(time, format = "%H:%M:%S")) %>%
        select(c("time", "capacity")) %>%
        group_by(time) %>%
        summarise(mean_capacity = mean(capacity, na.rm = TRUE)) %>%
        mutate(time2 = paste(today(), time) %>% as_datetime()) %>%
        ggplot(aes(time2, mean_capacity)) +
        geom_point() +
        ggtitle(day) +
        ylim(0, 100) +
        scale_x_datetime(
          breaks = scales::date_breaks("4 hours"),
          date_labels = "%H:%M"
        ) +
        xlab("time of day")
    )
  }
  output$plot_mon <- plot_day("Monday", 1)
  output$plot_tue <- plot_day("Tuesday", 2)
  output$plot_wed <- plot_day("Wednesday", 3)
  output$plot_thu <- plot_day("Thursday", 4)
  output$plot_fri <- plot_day("Friday", 5)
  output$plot_sat <- plot_day("Saturday", 6)
  output$plot_sun <- plot_day("Sunday", 7)
}

shinyApp(ui, server)
