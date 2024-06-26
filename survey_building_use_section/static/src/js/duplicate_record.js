/** @odoo-module **/

import {registry} from "@web/core/registry";
const {Component, useState, onWillStart, useRef} = owl;
import {useService} from "@web/core/utils/hooks";

// const intervalId = setInterval(() => {
//     const linkElement = document.querySelector('a[data-menu-xmlid="survey_building_use_section.menu_survey_question_owl_article"][title="."]');
//     if (linkElement) {
//         linkElement.style.color = '#66598f';
//         linkElement.removeAttribute('title');

//         linkElement.style.setProperty('background-color', 'initial', 'important');
//         linkElement.style.setProperty('text-decoration', 'none', 'important');

//         linkElement.style.cursor = 'default';

//         clearInterval(intervalId);
//     }
// }, 10);

export class OwlArticleList extends Component {
  setup() {
    this.state = useState({
      article: {name: "", error_text: "", description: "", question_normative_id: {}},
      articleList: [],
      isEdit: false,
      activeId: false,
    });
    this.orm = useService("orm");
    this.model = "survey.question.article";
    this.searchInput = useRef("search-input");

    onWillStart(async () => {
      await this.getAllArticles();
    });
  }

  async getAllArticles() {
    this.state.articleList = await this.orm.searchRead(
      this.model,
      [],
      ["id", "name", "error_text", "description", "question_normative_id"]
    );
  }

  addArticle() {
    this.resetForm();
    this.state.activeId = false;
    this.state.isEdit = false;
  }

  async editArticle(article, e, column) {
    try {
      const updatedData = {};

      if (column === "question_normative_id" && parseInt(e.target.value)) {
        updatedData[column] = parseInt(e.target.value);
      } else if (column !== "question_normative_id") {
        updatedData[column] = e.target.innerText;
      }
      await this.orm.write(this.model, [article.id], updatedData);
      await this.getAllArticles();
    } catch (error) {
      console.error("An error occurred while updating the article:", error);
    }
  }
  async duplicateArticle(article) {
    const duplicatedArticle = Object.assign({}, article);
    duplicatedArticle.id = false;
    duplicatedArticle.question_normative_id = article.question_normative_id[0];
    await this.orm.create(this.model, [duplicatedArticle]);
    await this.getAllArticles();
  }

  resetForm() {
    this.state.article = {
      name: "",
      error_text: "",
      description: "",
      question_normative_id: {},
    };
  }

  async deleteArticle(article) {
    await this.orm.unlink(this.model, [article.id]);
    await this.getAllArticles();
  }

  async searchArticles() {
    const text = this.searchInput.el.value;
    this.state.articleList = await this.orm.searchRead(
      this.model,
      [["name", "ilike", text]],
      ["id", "name", "error_text", "description", "question_normative_id"]
    );
  }
}

OwlArticleList.template = "survey_building_use_section.ArticleList";
registry
  .category("actions")
  .add("survey_building_use_section.action_article_list_js", OwlArticleList);
