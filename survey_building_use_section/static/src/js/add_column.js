// /** @odoo-module **/

// import { registry } from '@web/core/registry';
// const { Component, useState, onWillStart, useRef } = owl;
// import { ListRenderer } from "@web/views/list/list_renderer";

// export class ExtendListRenderer extends ListRenderer {
//     setup() {
//         super.setup();
//         this.allColumns++;
//     }

//     async getAllArticles() {
//         this.state.articleList = await this.orm.searchRead(this.model, [], ["name", "error_text", "description", "question_normative_id"])
//     }

//     addArticle() {
//         this.resetForm()
//         this.state.activeId = false
//         this.state.isEdit = false
//     }

//     async editArticle(article, e, column) {
//         try {
//             const updatedData = {};
//             updatedData[column] = e.target.innerText;
//             await this.orm.write(this.model, [article.id], updatedData);
//             await this.getAllArticles();
//         } catch (error) {
//             console.error("An error occurred while updating the article:", error);
//         }
//     }

//     async duplicateArticle(article) {
//         const duplicatedArticle = Object.assign({}, article);
//         duplicatedArticle.id = false;
//         duplicatedArticle.question_normative_id = (article.question_normative_id[0])
//         await this.orm.create(this.model, [duplicatedArticle]);
//         await this.getAllArticles();
//     }

//     async saveArticle() {

//         if (!this.state.isEdit) {
//             await this.orm.create(this.model, [this.state.article])
//             this.resetForm()
//         } else {
//             await this.orm.write(this.model, [this.state.activeId], this.state.article)
//         }

//         await this.getAllArticles()
//     }

//     resetForm() {
//         this.state.article = { name: "", error_text: "", description: "", question_normative_id: {} }
//     }

//     async deleteArticle(article) {
//         await this.orm.unlink(this.model, [article.id])
//         await this.getAllArticles()
//     }

//     async searchArticles() {
//         const text = this.searchInput.el.value
//         this.state.articleList = await this.orm.searchRead(this.model, [['name', 'ilike', text]], ["name", "error_text", "description", "question_normative_id"])
//     }

//     async toggleArticle(e, article) {
//         await this.orm.write(this.model, [article.id], { completed: e.target.checked })
//         await this.getAllArticles()
//     }

//     async updateColor(e, article) {
//         await this.orm.write(this.model, [article.id], { color: e.target.value })
//         await this.getAllArticles()
//     }
// }

// OwlArticleList.template = 'survey_building_use_section.ArticleList'
// registry.category('actions').add('survey_building_use_section.action_article_list_js', ListRenderer)
